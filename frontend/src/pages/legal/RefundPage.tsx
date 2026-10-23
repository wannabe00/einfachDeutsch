import { SITE_NAME } from "@/lib/site"
import { Clause, ContactLink, LegalLayout } from "./LegalLayout"

export default function RefundPage() {
  return (
    <LegalLayout
      title="Refund Policy"
      intro={`How cancelling and refunds work for ${SITE_NAME} Premium.`}
    >
      <Clause title="Free trial">
        <p>
          If Premium starts with a free trial, you're not charged when you cancel before the trial
          ends.
        </p>
      </Clause>
      <Clause title="Cancelling">
        <p>
          Cancel any time in Settings. Premium stays active until the end of the period you've paid
          for and then simply doesn't renew.
        </p>
      </Clause>
      <Clause title="Refunds">
        <p>
          <strong>First payment:</strong> if Premium isn't for you, ask within 14 days of your first
          payment and you get a full refund, no questions asked.
        </p>
        <p>
          <strong>Renewals:</strong> we don't refund partial periods, but if you were charged for a
          renewal you didn't want, write within 14 days and we'll sort it out fairly. Refunds required
          by consumer law are always given.
        </p>
      </Clause>
      <Clause title="How to ask">
        <p>
          E-mail <ContactLink /> from your account's e-mail address. Refunds go back to the original
          payment method, usually within 5 to 10 days.
        </p>
      </Clause>
    </LegalLayout>
  )
}
