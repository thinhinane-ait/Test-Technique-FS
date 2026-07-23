// src/services/comments.ts

export async function postComment(id: number, author: string, message: string) {
  const res = await fetch(`/api/incidents/${id}/comments`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ author, message }),
  });
   const result = await res.json();

  if (!res.ok) {
    throw new Error(
      result.message || "Impossible d'ajouter le commentaire"
    );
  }

  return result;
}
