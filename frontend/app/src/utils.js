export function formatDateTime(datetime) {
    const date = new Date(datetime);
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return date.toLocaleString(undefined, options);
  }
  