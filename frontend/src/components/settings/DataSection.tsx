import { Link } from "react-router-dom"

import { exportMyData } from "@/api/account"
import { Button } from "@/components/ui/button"
import { Section } from "./primitives"

/** Export-my-data (downloads a JSON file) + a link to the privacy policy. */
export function DataSection() {
  async function handleExport() {
    const data = await exportMyData()
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "my-data.json"
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <Section title="Your data">
      <div className="flex flex-wrap gap-2">
        <Button variant="outline" onClick={handleExport}>
          Export my data
        </Button>
        <Button variant="outline" asChild>
          <Link to="/privacy">Privacy policy</Link>
        </Button>
      </div>
    </Section>
  )
}
