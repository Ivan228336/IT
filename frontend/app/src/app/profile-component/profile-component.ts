import { Component, inject, OnInit, signal } from '@angular/core';
import { AuthService } from '../shared/services/auth-service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-profile-component',
  imports: [],
  templateUrl: './profile-component.html',
  styleUrl: './profile-component.scss',
})
export class ProfileComponent implements OnInit {
  private auth = inject(AuthService);
  private router = inject(Router);
  public token = signal<string | null>(null);
  public refresh = signal<string | null>(null);

  ngOnInit(): void {
    const token = this.auth.token;
    if (token) {
      this.token.set(token);
      this.refresh.set(this.auth.refresh);
    } else {
      this.router.navigate(['/auth/login']);
    }
  }
}
