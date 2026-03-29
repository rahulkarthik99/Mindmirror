import { Groq } from "groq-sdk";

const groq = new Groq({
  apiKey: process.env.GROQ_API_KEY,
});

export const getAiResponse = async (messages: { role: string; content: string }[]) => {
  try {
    const formattedMessages: any[] = [
      {
        role: "system",
        content: `You are MindMirror — a thoughtful psychological reflection partner.

Your goal is to help users understand their thoughts with clarity and emotional awareness.
Your personality: calm, curious, insightful, and compassionate.

You are NOT a clinical therapist.
Your role is to help users explore their inner world through reflection and thoughtful questioning.

Conversation principles:
• Avoid generic therapy clichés
• Avoid robotic or academic language
• Keep responses between 3-5 sentences
• Speak like a thoughtful mentor

Focus only on the user's thoughts and emotional experience. Do not talk about general knowledge, coding, politics, or other unrelated topics.`,
      },
      ...messages.map((m) => ({ role: m.role as "user" | "assistant" | "system", content: m.content })),
    ];

    const chatCompletion = await groq.chat.completions.create({
      messages: formattedMessages,
      model: "mixtral-8x7b-32768",
      temperature: 0.8,
      max_tokens: 500,
    });

    return chatCompletion.choices[0]?.message?.content || "I apologize, but I am unable to respond right now.";
  } catch (error) {
    console.error("Groq AI Error:", error);
    throw new Error("Failed to generate response from AI");
  }
};
