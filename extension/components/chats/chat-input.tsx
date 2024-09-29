import { useState, type ChangeEvent, type FormEvent } from "react"

type Props = {
  onSubmit(i: string, cb?: () => void): void
}

function ChatInput({ onSubmit }: Props) {
  const [text, setText] = useState("")

  function handleInputChange(e: ChangeEvent<HTMLTextAreaElement>) {
    const textarea = e.target
    textarea.style.height = "auto"
    textarea.style.height = `${textarea.scrollHeight}px`

    setText(e.target.value.slice(0, 280))
  }

  function onSubmitForm(e: FormEvent<HTMLFormElement>) {
    e.preventDefault()

    onSubmit(text)
  }

  return (
    <div id="chat-input-container">
      <form id="chat-input" onSubmit={onSubmitForm}>
        <textarea
          id="chat-textarea"
          value={text}
          onChange={handleInputChange}
          placeholder="..."
          rows={1}></textarea>
        <button id="chat-send-btn">Send</button>
      </form>
    </div>
  )
}

export default ChatInput
