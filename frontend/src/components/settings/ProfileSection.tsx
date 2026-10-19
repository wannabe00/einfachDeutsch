import { useRef, useState } from "react";

import { useAuth } from "@/contexts/AuthContext";
import { updateProfile, uploadAvatar } from "@/api/account";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { errorText } from "@/lib/apiError";
import { Select } from "@/components/ui/Select";
import { Field, Msg, Section } from "./primitives";

const REASONS = [
  { value: "", label: "Choose…" },
  { value: "work", label: "Work" },
  { value: "study", label: "Study" },
  { value: "living", label: "Living in a German-speaking country" },
  { value: "family", label: "Family or partner" },
  { value: "travel", label: "Travel" },
  { value: "exam", label: "An exam or visa" },
  { value: "fun", label: "For fun" },
];
const EXAMS = [
  { value: "", label: "None yet" },
  ...["A1", "A2", "B1", "B2", "C1", "C2"].map((l) => ({
    value: l,
    label: `Goethe-Zertifikat ${l}`,
  })),
];

/** Name/surname/username/birthday + avatar upload, and a few facts about
    the learner (stored in `preferences`, used later to personalise). */
export function ProfileSection() {
  const { user, refreshUser } = useAuth();
  const [firstName, setFirstName] = useState(user?.first_name ?? "");
  const [lastName, setLastName] = useState(user?.last_name ?? "");
  const [username, setUsername] = useState(user?.username ?? "");
  const [birthday, setBirthday] = useState(user?.birthday ?? "");
  const prefs = (user?.preferences ?? {}) as Record<string, string | undefined>;
  const [nativeLanguage, setNativeLanguage] = useState(
    prefs.native_language ?? "",
  );
  const [reason, setReason] = useState(prefs.learning_reason ?? "");
  const [exam, setExam] = useState(prefs.target_exam ?? "");
  const [examDate, setExamDate] = useState(prefs.target_date ?? "");
  const [location, setLocation] = useState(prefs.location ?? "");
  const [msg, setMsg] = useState("");
  const [error, setError] = useState("");
  const avatarInput = useRef<HTMLInputElement>(null);

  async function saveProfile() {
    setMsg("");
    setError("");
    try {
      await updateProfile({
        first_name: firstName,
        last_name: lastName,
        username,
        birthday: birthday || null,
        preferences: {
          native_language: nativeLanguage.trim(),
          learning_reason: reason,
          target_exam: exam,
          target_date: exam ? examDate : "",
          location: location.trim(),
        },
      });
      await refreshUser();
      setMsg("Saved.");
    } catch (e) {
      setError(errorText(e));
    }
  }

  async function onAvatarPick(file: File) {
    setError("");
    try {
      await uploadAvatar(file);
      await refreshUser();
      setMsg("Picture updated.");
    } catch (e) {
      setError(errorText(e));
    }
  }

  return (
    <>
      <Section title="Profile">
        <div className="flex items-center gap-4">
          <div className="flex size-16 items-center justify-center overflow-hidden rounded-full bg-primary text-2xl font-extrabold text-primary-foreground">
            {user?.avatar_url ? (
              <img
                src={user.avatar_url}
                alt=""
                className="size-full object-cover"
              />
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
                const f = e.target.files?.[0];
                if (f) onAvatarPick(f);
              }}
            />
            <Button
              variant="secondary"
              size="sm"
              onClick={() => avatarInput.current?.click()}
            >
              Change picture
            </Button>
          </div>
        </div>

        <div className="mt-5 grid gap-4 sm:grid-cols-2">
          <Field label="First name">
            <Input
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
            />
          </Field>
          <Field label="Surname">
            <Input
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
            />
          </Field>
          <Field label="Username (changeable every 30 days)">
            <Input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </Field>
          <Field label="Birthday">
            <Input
              type="date"
              value={birthday ?? ""}
              onChange={(e) => setBirthday(e.target.value)}
            />
          </Field>
          <Field label="Email (not editable)">
            <Input value={user?.email ?? ""} disabled />
          </Field>
        </div>
      </Section>

      <Section title="About your learning">
        <p className="-mt-2 mb-4 text-sm text-muted-foreground">
          Optional. Later this helps tailor examples, the AI tutor and an exam
          countdown to you.
        </p>
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Native language">
            <Input
              value={nativeLanguage}
              onChange={(e) => setNativeLanguage(e.target.value)}
              placeholder="e.g. Georgian"
              maxLength={60}
            />
          </Field>
          <Field label="Why are you learning German?">
            <Select
              label="Why are you learning German?"
              value={reason}
              onChange={setReason}
              options={REASONS}
            />
          </Field>
          <Field label="Exam you're aiming for">
            <Select
              label="Exam you're aiming for"
              value={exam}
              onChange={setExam}
              options={EXAMS}
            />
          </Field>
          <Field label="When (month)">
            <Input
              type="month"
              value={examDate}
              onChange={(e) => setExamDate(e.target.value)}
              disabled={!exam}
            />
          </Field>
          <Field label="Where you live">
            <Input
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="e.g. Tbilisi, Georgia"
              maxLength={80}
            />
          </Field>
        </div>
      </Section>

      {error && <Msg tone="danger">{error}</Msg>}
      {msg && <Msg tone="success">{msg}</Msg>}
      <Button size="lg" className="self-start" onClick={saveProfile}>
        Save profile
      </Button>
    </>
  );
}
