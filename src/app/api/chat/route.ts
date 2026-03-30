import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth.config";
import { prisma } from "@/lib/prisma";
import { getAiResponse } from "@/services/ai";

export async function POST(req: Request) {
  try {
    const session = await getServerSession(authOptions);

    if (!session || !session.user?.id) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const { content, conversationId } = await req.json();

    if (!content) {
      return NextResponse.json({ error: "Message content is required" }, { status: 400 });
    }

    const userId = session.user.id;

    // Fetch user and check limits
    const user = await prisma.user.findUnique({
      where: { id: userId },
      include: { subscription: true },
    });

    if (!user) {
      return NextResponse.json({ error: "User not found" }, { status: 404 });
    }

    const isPro = user.subscription?.plan === "PRO";

    // Simple free tier limit: 20 messages
    if (!isPro && user.messagesCount >= 20) {
      return NextResponse.json({
        error: "Message limit reached",
        code: "LIMIT_REACHED"
      }, { status: 403 });
    }

    // Get or create conversation
    let currentConversationId = conversationId;

    if (!currentConversationId) {
      const newConv = await prisma.conversation.create({
        data: {
          userId,
          title: content.substring(0, 30) + "...",
        },
      });
      currentConversationId = newConv.id;
    }

    // Save user message
    await prisma.message.create({
      data: {
        conversationId: currentConversationId,
        role: "user",
        content,
      },
    });

    // Increment user message count
    await prisma.user.update({
      where: { id: userId },
      data: { messagesCount: { increment: 1 } },
    });

    // Get chat history for context
    const recentMessages = await prisma.message.findMany({
      where: { conversationId: currentConversationId },
      orderBy: { createdAt: "asc" },
      take: 10,
    });

    const formattedHistory = recentMessages.map((m) => ({
      role: m.role,
      content: m.content,
    }));

    // Get AI Response
    const aiResponseContent = await getAiResponse(formattedHistory);

    // Save AI message
    const aiMessage = await prisma.message.create({
      data: {
        conversationId: currentConversationId,
        role: "assistant",
        content: aiResponseContent,
      },
    });

    return NextResponse.json({
      message: aiMessage,
      conversationId: currentConversationId,
      messagesRemaining: isPro ? "Unlimited" : Math.max(0, 20 - (user.messagesCount + 1)),
    });

  } catch (error) {
    console.error("[CHAT_ERROR]", error);
    return NextResponse.json({ error: "Internal Error" }, { status: 500 });
  }
}

export async function GET(req: Request) {
  try {
    const session = await getServerSession(authOptions);

    if (!session || !session.user?.id) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const userId = session.user.id;

    const { searchParams } = new URL(req.url);
    const conversationId = searchParams.get("conversationId");

    if (!conversationId) {
      // Get all conversations for user
      const conversations = await prisma.conversation.findMany({
        where: { userId },
        orderBy: { updatedAt: "desc" },
      });
      return NextResponse.json(conversations);
    }

    // Verify conversation belongs to user
    const conversation = await prisma.conversation.findUnique({
      where: { id: conversationId },
    });

    if (!conversation || conversation.userId !== userId) {
      return NextResponse.json({ error: "Not found" }, { status: 404 });
    }

    const messages = await prisma.message.findMany({
      where: { conversationId },
      orderBy: { createdAt: "asc" },
    });

    return NextResponse.json({ conversation, messages });
  } catch (error) {
    console.error("[CHAT_GET_ERROR]", error);
    return NextResponse.json({ error: "Internal Error" }, { status: 500 });
  }
}
