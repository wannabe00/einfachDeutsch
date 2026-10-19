import { Link } from "react-router-dom"

import { MIN_AGE, OPERATOR_COUNTRY, OPERATOR_NAME, SITE_NAME } from "@/lib/site"
import { Clause, ContactLink, LegalLayout } from "./LegalLayout"

export default function PrivacyPage() {
  return (
    <LegalLayout
      title="Privacy Policy"
      intro={`What ${SITE_NAME} collects, why, who else handles it, and how you control it.`}
    >
      <Clause title="Who is responsible">
        <p>
          {SITE_NAME} is run by {OPERATOR_NAME}, an individual based in {OPERATOR_COUNTRY}, who is
          responsible for your personal data. Questions or requests: <ContactLink />.
        </p>
      </Clause>
      <Clause title="What we collect and why">
        <ul>
          <li>
            <strong>Account:</strong> from Google or GitHub your name, e-mail address and account id;
            then the username and password you choose (stored only as a secure hash), and optionally a
            profile picture and birthday. Needed to give you an account.
          </li>
          <li>
            <strong>Learning:</strong> your level, lesson and exercise progress, reviews, streaks,
            saved words, written texts and scores. Needed to run the course.
          </li>
          <li>
            <strong>Optional profile facts</strong> you choose to add (native language, why you learn
            German, exam goal, where you live), kept to tailor the course later.
          </li>
          <li>
            <strong>AI features (Premium):</strong> your chat messages and the tutor's answers, Talk
            to AI transcripts and reports, and texts sent for AI grading are stored so you can read
            them again. Voice is never stored: in Talk to AI and the chat microphone, audio goes to the
            AI provider only to be understood.
          </li>
          <li>
            <strong>Security and reliability:</strong> sign-in events (account id and IP address) and
            technical error reports without your name or e-mail, to protect accounts and fix problems.
          </li>
          <li>
            <strong>Payments</strong> (when Premium can be bought): handled by Stripe; we only keep
            your subscription status, never your card details.
          </li>
        </ul>
        <p>
          We use your data to provide the service, keep it secure and answer you. We don't sell it,
          don't use it for advertising, and don't send marketing e-mails.
        </p>
      </Clause>
      <Clause title="Services that process data for us">
        <ul>
          <li>Google and GitHub: sign-in.</li>
          <li>
            Google (Gemini): the AI tutor, AI grading, Talk to AI and speech-to-text. While {SITE_NAME}{" "}
            uses Google's free AI tier, Google may use what you send to these features to improve its
            products, so please don't share personal or sensitive information in them.
          </li>
          <li>Microsoft (Azure Speech): reading AI answers aloud.</li>
          <li>Vercel, Render and Neon: hosting the website, the server and the database.</li>
          <li>Cloudinary: profile pictures.</li>
          <li>Brevo: password-reset e-mails.</li>
          <li>Sentry: error reports (no names, e-mails or IP addresses kept).</li>
          <li>Stripe: payments, once Premium can be bought.</li>
          <li>
            Pictures and video previews load directly from their sources (YouTube, Wikimedia,
            museum collections, Unsplash, Pexels, German broadcasters), which see your IP address as
            any website does. No videos are embedded; video links open on the provider's site.
          </li>
        </ul>
        <p>
          Some of them process data outside your country, including in the United States and the
          European Union, under their own data-protection terms.
        </p>
      </Clause>
      <Clause title="How long we keep it">
        <p>
          Account and learning data: until you delete your account. Chats and talks: until you delete
          them or your account. Sign-in logs and error reports: a few weeks at most. Payment records:
          as long as tax law requires.
        </p>
      </Clause>
      <Clause title="Your rights">
        <p>
          You can see, correct, export and delete your data at any time: edit your profile in
          Settings, download everything with <strong>Settings → Account → Export my data</strong>,
          and delete your account there too. You can also object to or ask us to limit processing,
          and complain to a data-protection authority (in Georgia the Personal Data Protection
          Service; in the EU the authority of your country). For anything else, write to{" "}
          <ContactLink />.
        </p>
      </Clause>
      <Clause title="Children">
        <p>
          {SITE_NAME} is for people aged {MIN_AGE} and over. If you believe a younger person has made
          an account, tell us and we'll delete it.
        </p>
      </Clause>
      <Clause title="Cookies and changes">
        <p>
          We don't use advertising or tracking cookies; see the <Link to="/cookies">Cookie Policy</Link>.
          If this policy changes in an important way, we'll say so on the site.
        </p>
      </Clause>
    </LegalLayout>
  )
}
