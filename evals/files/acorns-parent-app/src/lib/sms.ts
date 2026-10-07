import AfricasTalking from "africastalking";

const at = AfricasTalking({ apiKey: process.env.AT_KEY!, username: "acorns" });

export async function sendFeeReminder(phone: string, pupilName: string, balance: number) {
  await at.SMS.send({ to: [phone], message: `Fee reminder for ${pupilName}: KES ${balance} due.` });
}
