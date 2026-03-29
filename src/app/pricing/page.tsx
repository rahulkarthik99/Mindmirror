"use client";

import { useState } from "react";
import { Check } from "lucide-react";
import { PayPalScriptProvider, PayPalButtons } from "@paypal/react-paypal-js";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";

export default function PricingPage() {
  const { data: session } = useSession();
  const router = useRouter();
  const [isYearly, setIsYearly] = useState(false);
  const [paymentSuccess, setPaymentSuccess] = useState(false);

  const handleApprove = async (data: any, actions: any) => {
    // Note: In production, verify the transaction on the server side
    setPaymentSuccess(true);
    setTimeout(() => {
      router.push("/dashboard/chat");
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center">
          <h2 className="text-3xl font-extrabold text-gray-900 dark:text-white sm:text-4xl">
            Simple, transparent pricing
          </h2>
          <p className="mt-4 text-xl text-gray-600 dark:text-gray-300">
            Choose the plan that best fits your needs.
          </p>
        </div>

        <div className="mt-12 flex justify-center">
          <div className="relative flex items-center p-1 bg-gray-200 dark:bg-gray-800 rounded-xl">
            <button
              onClick={() => setIsYearly(false)}
              className={`${
                !isYearly ? "bg-white dark:bg-gray-700 shadow-sm" : "text-gray-500 dark:text-gray-400"
              } relative w-1/2 rounded-lg py-2 px-6 text-sm font-medium transition-colors`}
            >
              Monthly
            </button>
            <button
              onClick={() => setIsYearly(true)}
              className={`${
                isYearly ? "bg-white dark:bg-gray-700 shadow-sm" : "text-gray-500 dark:text-gray-400"
              } relative w-1/2 rounded-lg py-2 px-6 text-sm font-medium transition-colors`}
            >
              Annually <span className="text-green-500 ml-1">-20%</span>
            </button>
          </div>
        </div>

        {paymentSuccess && (
          <div className="mt-8 bg-green-50 border border-green-200 text-green-800 rounded-lg p-4 text-center max-w-md mx-auto">
            Payment successful! Upgrading your account... Redirecting to dashboard.
          </div>
        )}

        <div className="mt-12 max-w-lg mx-auto grid gap-8 lg:grid-cols-2 lg:max-w-none">
          {/* Free Tier */}
          <div className="flex flex-col bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 p-8">
            <div className="mb-8">
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white">Free</h3>
              <p className="mt-4 text-gray-500 dark:text-gray-400">Perfect for trying out MindMirror.</p>
              <div className="mt-6 flex items-baseline text-5xl font-extrabold text-gray-900 dark:text-white">
                $0
                <span className="ml-1 text-xl font-medium text-gray-500 dark:text-gray-400">/mo</span>
              </div>
            </div>
            <ul className="flex-1 space-y-4">
              {["20 AI messages per month", "Basic emotion analysis", "Standard response speed", "Community support"].map(
                (feature) => (
                  <li key={feature} className="flex items-start">
                    <Check className="flex-shrink-0 h-6 w-6 text-green-500" />
                    <span className="ml-3 text-gray-500 dark:text-gray-400">{feature}</span>
                  </li>
                )
              )}
            </ul>
            <button
              onClick={() => router.push(session ? "/dashboard/chat" : "/login")}
              className="mt-8 block w-full bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white hover:bg-gray-200 dark:hover:bg-gray-600 font-semibold py-3 px-4 rounded-xl text-center transition-colors"
            >
              {session ? "Current Plan" : "Get Started"}
            </button>
          </div>

          {/* Pro Tier */}
          <div className="flex flex-col bg-blue-600 rounded-2xl shadow-xl p-8 relative overflow-hidden">
            <div className="absolute top-0 right-0 -mt-4 -mr-4 w-24 h-24 bg-blue-500 rounded-full opacity-50" />
            <div className="mb-8 relative z-10">
              <h3 className="text-2xl font-bold text-white">Pro</h3>
              <p className="mt-4 text-blue-100">For deep reflection and unlimited access.</p>
              <div className="mt-6 flex items-baseline text-5xl font-extrabold text-white">
                ${isYearly ? "9" : "12"}
                <span className="ml-1 text-xl font-medium text-blue-200">/mo</span>
              </div>
            </div>
            <ul className="flex-1 space-y-4 relative z-10">
              {[
                "Unlimited AI messages",
                "Advanced cognitive distortion detection",
                "Priority response speed",
                "Detailed monthly insights",
                "Email support",
              ].map((feature) => (
                <li key={feature} className="flex items-start">
                  <Check className="flex-shrink-0 h-6 w-6 text-blue-300" />
                  <span className="ml-3 text-white">{feature}</span>
                </li>
              ))}
            </ul>

            <div className="mt-8 relative z-10">
              {!session ? (
                <button
                  onClick={() => router.push("/login")}
                  className="block w-full bg-white text-blue-600 hover:bg-blue-50 font-semibold py-3 px-4 rounded-xl text-center transition-colors"
                >
                  Sign in to Upgrade
                </button>
              ) : (
                <PayPalScriptProvider options={{ clientId: process.env.NEXT_PUBLIC_PAYPAL_CLIENT_ID || "test" }}>
                  <PayPalButtons
                    style={{ layout: "vertical", shape: "rect" }}
                    createOrder={(data, actions) => {
                      return actions.order.create({
                        intent: "CAPTURE",
                        purchase_units: [
                          {
                            amount: {
                              value: isYearly ? "108.00" : "12.00",
                              currency_code: "USD",
                            },
                            // Pass the userId so we can link the payment to the user in the webhook!
                            custom_id: (session.user as any)?.id,
                          },
                        ],
                      });
                    }}
                    onApprove={async (data, actions) => {
                      if (actions.order) {
                        await actions.order.capture();
                      }
                      await handleApprove(data, actions);
                    }}
                  />
                </PayPalScriptProvider>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}