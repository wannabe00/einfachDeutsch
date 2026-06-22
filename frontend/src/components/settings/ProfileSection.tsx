import { useRef, useState } from "react"

import { useAuth } from "@/contexts/AuthContext"
import { updateProfile, uploadAvatar } from "@/api/account"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { errorText } from "@/lib/apiError"
import { Field, Msg, Section } from "./primitives"

/** Name/surname/username/birthday/phone + avatar upload. */
export function ProfileSection() {
  const { user, refreshUser } = useAuth()
  const [firstName, setFirstName] = useState(user?.first_name ?? "")
  const [lastName, setLastName] = useState(user?.last_name ?? "")
  const [username, setUsername] = useState(user?.username ?? "")
  const [birthday, setBirthday] = useState(user?.birthday ?? "")
  const [phone, setPhone] = useState(user?.phone ?? "")
  const [msg, setMsg] = useState("")
  const [error, setError] = useState("")
  const avatarInput = useRef<HTMLInputElement>(null)

  async function saveProfile() {
    setMsg("")
    setError("")
    try {
      await updateProfile({
        first_name: firstName,
        last_name: lastName,
        username,
        birthday: birthday || null,
        phone,
      })
      await refreshUser()
      setMsg("Saved.")
    } catch (e) {
      setError(errorText(e))
    }
  }

  async function onAvatarPick(file: File) {
    setError("")
    try {
      await uploadAvatar(file)
      await refreshUser()
      setMsg("Picture updated.")
    } catch (e) {
      setError(errorText(e))
    }
  }

  return (
    <Section title="Profile">
      <div className="flex items-center gap-4">
        <div className="flex size-16 items-center justify-center overflow-hidden rounded-full bg-accent/15 text-xl font-bold text-accent">
          {user?.avatar_url ? (
            <img src={user.avatar_url} alt="" className="size-full object-cover" />
          ) : (
            (user?.username ?? "?").charAt(0).toUpperCase()
          )}
        </div>
        <div>
          <input
            ref={avatarInput}
            type="file"
            accept="image/*"
            className="hidden"
            onChange={(e) => {
              const f = e.target.files?.[0]
              if (f) onAvatarPick(f)
            }}
          />
          <Button variant="outline" size="sm" onClick={() => avatarInput.current?.click()}>
            Change picture
          </Button>
        </div>
      </div>

      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        <Field label="First name">
          <Input value={firstName} onChange={(e) => setFirstName(e.target.value)} />
        </Field>
        <Field label="Surname">
          <Input value={lastName} onChange={(e) => setLastName(e.target.value)} />
        </Field>
        <Field label="Username (changeable every 30 days)">
          <Input value={username} onChange={(e) => setUsername(e.target.value)} />
        </Field>
        <Field label="Birthday">
          <Input type="date" value={birthday ?? ""} onChange={(e) => setBirthday(e.target.value)} />
        </Field>
        <Field label="Phone">
          <Input type="tel" value={phone} onChange={(e) => setPhone(e.target.value)} />
        </Field>
        <Field label="Email (not editable)">
          <Input value={user?.email ?? ""} disabled />
        </Field>
      </div>
      {error && <Msg tone="danger">{error}</Msg>}
      {msg && <Msg tone="success">{msg}</Msg>}
      <Button className="mt-3 self-start" onClick={saveProfile}>
        Save profile
      </Button>
    </Section>
  )
}
