import { Link } from "react-router-dom"

import { MIN_AGE, OPERATOR_COUNTRY, OPERATOR_NAME, SITE_NAME } from "@/lib/site"
import { Clause, ContactLink, LegalLayout } from "./LegalLayout"

export default function TermsPage() {
  return (
    <LegalLayout
      title="Terms of Service"
      intro={`The rules for using ${SITE_NAME}. By creating an account you agree to them.`}
    >
      <Clause title="The service">
        <p>
          {SITE_NAME} is an online German course with lessons, practice and, for Premium members, AI
          tools. It is run by {OPERATOR_NAME} ({OPERATOR_COUNTRY}); contact: <ContactLink />. We may
          improve, change or remove features over time.
        </p>
      </Clause>
      <Clause title="Your account">
        <p>
          You must be at least {MIN_AGE}. You sign up with Google or GitHub, and you're responsible for
          keeping your login safe (two-factor login is available in Settings). One account per person;
          don't share it.
        </p>
      </Clause>
      <Clause title="Fair use">
        <p>Please don't:</p>
        <ul>
          <li>break, overload or attack the site, or try to get around its limits or locks;</li>
          <li>copy the course content in bulk or use bots to scrape it;</li>
          <li>use the AI features for anything unlawful, harmful or unrelated to learning;</li>
          <li>upload content you don't have the right to share.</li>
        </ul>
        <p>We may suspend accounts that do, after a warning where reasonable.</p>
      </Clause>
      <Clause title="Premium and payments">
        <p>
          Premium adds unlimited lessons per day and the AI tools. It is a subscription, monthly or
          yearly, renewing automatically until you cancel; a free trial may come first. Prices are
          shown before you pay, and payments are handled by Stripe. You can cancel any time and keep
          Premium until the end of the paid period. Refunds: see the{" "}
          <Link to="/refunds">Refund Policy</Link>.
        </p>
      </Clause>
      <Clause title="AI answers">
        <p>
          The AI tutor, AI grading and Talk to AI can make mistakes. Use them as practice help, not
          as an official exam result or professional advice.
        </p>
      </Clause>
      <Clause title="Content">
        <p>
          The course material is ours and is for your personal learning. Texts you write stay yours;
          you let us store and process them to run the service.
        </p>
      </Clause>
      <Clause title="Liability">
        <p>
          We work to keep {SITE_NAME} correct and available but can't promise it will always be
          error-free or online. As far as the law allows, we aren't liable for indirect losses, and
          our total liability is limited to what you paid us in the last twelve months. Nothing here
          limits rights you have under consumer law that can't be waived.
        </p>
      </Clause>
      <Clause title="Ending and changes">
        <p>
          You can delete your account any time in Settings. If these terms change in an important
          way, we'll tell you on the site before the change applies. These terms are governed by the
          laws of {OPERATOR_COUNTRY}, without taking away protections of the consumer law where you
          live.
        </p>
      </Clause>
    </LegalLayout>
  )
}
