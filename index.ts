import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

console.log("Edge function 'telegram-task-update' is up and running!");

serve(async (req) => {
  // This is the secret you set with the Supabase CLI
  const BOT_SECRET = Deno.env.get("TELEGRAM_WEBHOOK_SECRET");

  // 1. Check if the request method is POST
  if (req.method !== "POST") {
    return new Response("Method Not Allowed", { status: 405 });
  }

  // 2. Verify the secret from the header
  const requestSecret = req.headers.get("x-bot-secret");
  if (requestSecret !== BOT_SECRET) {
    console.warn("Unauthorized request: Invalid secret received.");
    return new Response("Unauthorized", { status: 401 });
  }

  try {
    // 3. Parse the JSON body from the bot
    const body = await req.json();
    const { telegramId, taskKey, status, meta } = body;

    console.log(`Received task update for user ${telegramId}:`);
    console.log(`  Task: ${taskKey}, Status: ${status}`);
    console.log("  Metadata:", meta);

    // TODO: Add your logic here to update your main database.
    // Example:
    // const supabaseClient = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_ANON_KEY")!);
    // const { error } = await supabaseClient.from('user_tasks').update({ status: 'completed' }).eq('user_id', telegramId).eq('task_key', taskKey);
    // if (error) throw error;

    // 4. Return a success response
    return new Response(JSON.stringify({ message: "Update received successfully" }), {
      headers: { "Content-Type": "application/json" },
      status: 200,
    });
  } catch (error) {
    console.error("Error processing request:", error);
    return new Response(JSON.stringify({ error: "Internal Server Error", details: error.message }), {
      headers: { "Content-Type": "application/json" },
      status: 500,
    });
  }
});