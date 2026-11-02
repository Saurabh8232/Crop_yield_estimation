export function Loading({ text = "Loading data..." }) { return <div className="state-box"><span className="spinner" />{text}</div>; }
export function ErrorState({ message = "Unable to load data." }) { return <div className="state-box error-state">{message}</div>; }
export function EmptyState({ text = "No records available yet." }) { return <div className="state-box">{text}</div>; }
