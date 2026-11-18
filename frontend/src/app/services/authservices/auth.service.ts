import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, tap } from 'rxjs';


interface LoginResponse {
  access: string;
  refresh: string;
}

interface RefreshResponse {
  access: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private apiUrl = 'http://127.0.0.1:8000/api/auth/login/';

  constructor(private http: HttpClient) { }
  
  login(username:string, password :string): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(this.apiUrl, {
      username,
      password
    }).pipe(
    tap(response => {
      console.log('Full API response:', response);
      console.log('Access token:', response.access);
      console.log('Refresh token:', response.refresh);

      localStorage.setItem('access', response.access);
      localStorage.setItem('refresh', response.refresh);

      console.log('Storage:', localStorage.getItem('access'));
    })
    );
  }

  refreshToken(): Observable<RefreshResponse> {
  const refresh = localStorage.getItem('refresh');

  return this.http.post<RefreshResponse>(
    'http://127.0.0.1:8000/api/auth/refresh/',
    { refresh }
  ).pipe(
    tap(response => {
      localStorage.setItem('access', response.access);
    })
  );
}

  getProtectedData(): Observable<{ message: string; username: string }> {
  return this.http.get<{ message: string; username: string }>(
    'http://127.0.0.1:8000/api/protected/'
  );
}
}
  