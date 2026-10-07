import mixpanel from "mixpanel-browser";
import { initializeApp } from "firebase/app";
import { getMessaging } from "firebase/messaging";

mixpanel.init(process.env.NEXT_PUBLIC_MIXPANEL_TOKEN!);
export const app = initializeApp({ projectId: "acorns-parent" });
export const messaging = getMessaging(app);

export function trackSignup(guardian: { email?: string; phone: string }) {
  mixpanel.identify(guardian.phone);
  mixpanel.people.set({ $email: guardian.email, phone: guardian.phone });
}
