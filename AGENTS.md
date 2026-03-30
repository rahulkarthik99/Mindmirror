# MindMirror - Agent Guidelines

## Tech Stack & Architecture
- **Next.js 16 (App Router):** Follow modern App Router paradigms (`src/app/`, Server Components, Client Components where `use client` is needed).
- **TypeScript:** Strict typing preferred. Avoid using `any`. Extend NextAuth sessions using `src/types/next-auth.d.ts`.
- **Styling:** Tailwind CSS with modern utilities (`@tailwindcss/postcss`).
- **Database:** Prisma ORM connected to PostgreSQL. Migrations and schema changes must be well documented.
- **Authentication:** NextAuth (Auth.js) v4 with Google, Facebook, and Email/Password Credentials.

## Core Domain: Mental Wellness & AI Reflection
- **Purpose:** MindMirror is a psychological reflection tool, not a clinical therapist or a general AI assistant.
- **AI Behavior (Groq):** Responses must be calm, curious, and compassionate. Do NOT provide diagnoses or medical advice. Limit responses to 3-5 thoughtful sentences guiding the user to self-reflect.
- **Service Layer:** AI logic resides in `src/services/ai.ts` powered exclusively by Groq. **Do not use OpenAI.**

## Business Logic & Rules
1. **Free Tier:** Users start on a Free Tier limited to **20 AI messages**. This logic is enforced in the `POST /api/chat` route. Check the `messagesCount` column in the `User` model.
2. **Pro Tier:** Users can upgrade to "PRO" via PayPal. Pro users have unlimited messages.
3. **Payment Webhook:** PayPal webhooks are handled in `src/app/api/webhooks/paypal/route.ts`. The event `PAYMENT.CAPTURE.COMPLETED` updates the user's subscription in the database by mapping the `custom_id` passed during checkout to the user ID.

## Standard Development Workflows
- **Running locally:** Start the app using `npm run dev`.
- **Database Schema Changes:** Apply changes via `npm run db:push` in development (or `npx prisma migrate dev` in production contexts).
- **Build Checks:** Before committing, always run `npm run build` to catch TypeScript and Next.js optimization errors. Ensure components using hooks like `useSearchParams()` are wrapped in a `<Suspense>` boundary.