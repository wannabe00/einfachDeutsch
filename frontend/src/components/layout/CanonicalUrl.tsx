import { useEffect } from "react"
import { useLocation } from "react-router-dom"

const SITE_URL = (import.meta.env.VITE_SITE_URL as string).replace(/\/$/, "")

/** Keeps <link rel="canonical"> on the current page's own address, so search
    engines don't treat every page as a copy of the home page. */
export function CanonicalUrl() {
  const { pathname } = useLocation()
  useEffect(() => {
    document.querySelector('link[rel="canonical"]')?.setAttribute("href", `${SITE_URL}${pathname}`)
  }, [pathname])
  return null
}
