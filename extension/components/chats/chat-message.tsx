type Props = {
  type: "user" | "assistant"
  avatar_url: string
  name: string
  message: string
}

function ChatMessage({ avatar_url, type, name, message }: Props) {
  return (
    <div
      className={`chat-message ${type === "user" ? "user-message" : "assistant-message"}`}>
      {type === "assistant" && (
        <div className="message-author">
          <div className="message-avatar">
            <img className="avatar" src={avatar_url} alt={`${name}'s avatar`} />
          </div>
          <span className="message-author-name">{name}</span>
        </div>
      )}
      <div className="message-content">
        <p>{message}</p>
      </div>
    </div>
  )
}

export default ChatMessage
