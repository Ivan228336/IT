import { inject, Injectable } from '@angular/core';
import {
  EmailVerified,
  LoginSchemaIn,
  LoginSchemaOut,
  SuccessResponse,
  UserRegister,
} from './auth-service.types';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private http = inject(HttpClient);
  private apiUrl = '/api';

  register(body: UserRegister): Observable<SuccessResponse> {
    return this.http
      .post<SuccessResponse>(this.apiUrl + '/auth/register/', body)
      .pipe(tap((user) => console.log('Создан пользователь:', user)));
  }
  login(body: LoginSchemaIn): Observable<LoginSchemaOut> {
    return this.http
      .post<LoginSchemaOut>(this.apiUrl + '/auth/authorization', body)
      .pipe(
        tap((user) => {
          console.log('Пользователь залогинен:', user);
          this.token = user.access;
          this.refresh = user.refresh;
        })
      );
  }

  verifyEmail(token: string) {
    return this.http
      .post<EmailVerified>(this.apiUrl + '/auth/verify', { token: token })
      .pipe(
        tap((user) => {
          console.log('Пользователь верифицирован:', user);
          this.token = user.access;
          this.refresh = user.refresh;
        })
      );
  }

  get token(): string | null {
    return localStorage.getItem('token');
  }

  set token(token: string) {
    localStorage.setItem('token', token);
  }

  get refresh(): string | null {
    return localStorage.getItem('refresh');
  }

  set refresh(token: string) {
    localStorage.setItem('refresh', token);
  }
}
