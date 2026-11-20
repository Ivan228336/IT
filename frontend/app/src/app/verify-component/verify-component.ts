import { Component, inject, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../shared/services/auth-service';

@Component({
  selector: 'app-verify-component',
  imports: [],
  templateUrl: './verify-component.html',
  styleUrl: './verify-component.scss',
})
export class VerifyComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private auth = inject(AuthService);

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      const token = params['token'];
      if (token) {
        this.auth.verifyEmail(token).subscribe({
          next: (value) => {
            this.router.navigate(['/profile']);
          },
          error: (err) => {
            this.router.navigate(['/auth/login']);
          },
        });
      }
    });
  }
}
