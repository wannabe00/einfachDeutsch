import { useState } from "react"
import { Link } from "react-router-dom"
import { ArrowRight } from "lucide-react"

import { MUNICH_PHOTO } from "@/lib/photos"

export function Hero({
  name,
  level,
  lektion,
  dueToday,
  continueHref,
}: {
  name: string | null
  level: string
  lektion: number | null
  dueToday: number
  continueHref: string
}) {
  const [imgOk, setImgOk] = useState(true)
  const secondary =
    dueToday > 0
      ? { to: "/review", label: `Review ${dueToday} ${dueToday === 1 ? "word" : "words"}` }
      : { to: "/words", label: "Browse the Word Bank" }

  return (
    <section className="relative flex min-h-[300px] items-end overflow-hidden rounded-[24px] bg-[#222] text-white sm:min-h-[340px]">
      {imgOk && (
        <img
          src={MUNICH_PHOTO}
          alt="Munich's old town at sunset"
          onError={() => setImgOk(false)}
          className="absolute inset-0 size-full object-cover"
        />
      )}
      <div className="absolute inset-0 bg-gradient-to-t from-black/85 via-black/30 to-black/5" />
      <div className="relative flex flex-col gap-2.5 p-5 sm:p-8">
        <p className="text-[13px] font-semibold uppercase tracking-[0.04em] text-white/80">
          Level {level}
          {lektion !== null && ` · Lektion ${lektion}`}
        </p>
        <h1 className="text-[30px] font-extrabold leading-[1.05] sm:text-[44px]">
          Willkommen zurück{name ? `, ${name}` : ""}!
        </h1>
        <p className="text-white/85 sm:text-[17px]">
          {dueToday > 0
            ? `${dueToday} ${dueToday === 1 ? "word is" : "words are"} waiting for review.`
            : "Nothing due for review right now."}
        </p>
        <div className="mt-2 flex flex-wrap gap-2.5">
          <Link to={continueHref} className="d-btn d-btn-red">
            Continue learning
            <ArrowRight className="size-[18px]" aria-hidden="true" />
          </Link>
          <Link to={secondary.to} className="d-btn d-btn-glass">
            {secondary.label}
          </Link>
        </div>
      </div>
    </section>
  )
}
