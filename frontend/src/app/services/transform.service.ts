import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { ArchiveMatch, TransformResponse } from '../models/response.model';

interface StreamEvent {
  type: 'matches' | 'token' | 'done' | 'error' | 'blocked';
  matches?: ArchiveMatch[];
  ambient_track?: string;
  text?: string;
}

@Injectable({ providedIn: 'root' })
export class TransformService {
  constructor(private http: HttpClient) {}

  transform(userText: string): Observable<TransformResponse> {
    return this.http.post<TransformResponse>(`${environment.apiUrl}/api/transform`, {
      user_text: userText,
    });
  }

  transformStream(
    userText: string,
    onToken: (token: string) => void,
    onMatches: (matches: ArchiveMatch[], ambientTrack: string) => void,
    onDone: () => void,
    onError: () => void,
    onBlocked: () => void,
  ): void {
    fetch(`${environment.apiUrl}/api/transform/stream`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_text: userText }),
    })
      .then(async (response) => {
        if (!response.ok || !response.body) { onError(); return; }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const parts = buffer.split('\n\n');
          buffer = parts.pop() ?? '';

          for (const part of parts) {
            const line = part.trim();
            if (!line.startsWith('data: ')) continue;
            try {
              const event: StreamEvent = JSON.parse(line.slice(6));
              if (event.type === 'blocked') {
                onBlocked();
                return;
              } else if (event.type === 'matches' && event.matches) {
                onMatches(event.matches, event.ambient_track ?? '');
              } else if (event.type === 'token' && event.text) {
                onToken(event.text);
              } else if (event.type === 'done') {
                onDone();
              } else if (event.type === 'error') {
                onError();
              }
            } catch { /* malformed chunk — skip */ }
          }
        }
      })
      .catch(() => onError());
  }
}
