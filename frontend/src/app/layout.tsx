import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'ToDo Prioritizer - Get Clarity on What to Do Next',
  description: 'Break down your to-do list into actionable micro-steps and identify what to do next',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

