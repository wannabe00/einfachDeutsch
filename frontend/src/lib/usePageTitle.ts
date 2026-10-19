import { useEffect } from "react"

import { SITE_NAME } from "@/lib/site"

/** The browser tab and search result title: "Grammar · einfachDeutsch". */
export function usePageTitle(title: string | undefined) {
  useEffect(() => {
    if (!title) return
    const before = document.title
    document.title = `${title} · ${SITE_NAME}`
    return () => {
      document.title = before
    }
  }, [title])
}
