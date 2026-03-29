import { NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";

export async function POST(req: Request) {
  try {
    const body = await req.json();

    // Verify webhook signature in production
    // const signature = req.headers.get('paypal-transmission-sig');

    const eventType = body.event_type;

    if (eventType === "BILLING.SUBSCRIPTION.ACTIVATED" || eventType === "PAYMENT.CAPTURE.COMPLETED") {
      // In a real implementation, custom_id should be passed during checkout to link to the user.
      const customId = body.resource?.custom_id;
      const subscriptionId = body.resource?.id;

      if (customId && subscriptionId) {
        await prisma.subscription.upsert({
          where: { userId: customId },
          create: {
            userId: customId,
            paypalSubscriptionId: subscriptionId,
            plan: "PRO",
            status: "ACTIVE",
          },
          update: {
            paypalSubscriptionId: subscriptionId,
            plan: "PRO",
            status: "ACTIVE",
          },
        });
      }
    } else if (
      eventType === "BILLING.SUBSCRIPTION.CANCELLED" ||
      eventType === "BILLING.SUBSCRIPTION.EXPIRED"
    ) {
      const subscriptionId = body.resource?.id;

      if (subscriptionId) {
        await prisma.subscription.update({
          where: { paypalSubscriptionId: subscriptionId },
          data: { status: "CANCELLED", plan: "FREE" },
        });
      }
    }

    return NextResponse.json({ status: "success" });
  } catch (error) {
    console.error("PayPal Webhook Error:", error);
    return NextResponse.json({ error: "Webhook handler failed" }, { status: 500 });
  }
}
