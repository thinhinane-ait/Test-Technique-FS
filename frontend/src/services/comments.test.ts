// src/services/comments.test.ts

import { afterEach, describe, expect, it, vi } from "vitest";
import { postComment } from "./comments";

describe("postComment", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("envoie correctement le commentaire", async () => {
    const apiResponse = {
      data: {
        id: 12,
        author: "candidate@company.com",
        message: "Incident vérifié",
      },
    };

    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue({
        ok: true,
        json: async () => apiResponse,
      } as Response);

    const result = await postComment(
      3,
      "candidate@company.com",
      "Incident vérifié"
    );

    expect(fetchMock).toHaveBeenCalledWith(
      "/api/incidents/3/comments",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          author: "candidate@company.com",
          message: "Incident vérifié",
        }),
      }
    );

    expect(result).toEqual(apiResponse);
  });

  it("lance une erreur lorsque l'API échoue", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      ok: false,
      json: async () => ({
        message: "Le commentaire est obligatoire",
      }),
    } as Response);

    await expect(
      postComment(3, "candidate@company.com", "")
    ).rejects.toThrow("Le commentaire est obligatoire");
  });
});