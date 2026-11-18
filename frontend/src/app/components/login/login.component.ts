import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/authservices/auth.service';

@Component({
  selector: 'app-login',
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  username = '';
  password = '';
  errorMessage = '';
  successMessage = '';

  constructor(private authService: AuthService){}

  onLogin(): void {
    this.errorMessage = '';
    this.successMessage = '';

    this.authService.login(this.username, this.password).subscribe({
      next: () => {
        this.successMessage = 'Login successful! Tokens stored.';

        this.authService.getProtectedData().subscribe({
          next: (data) => {
            console.log('Protected API success:', data);
          },
          error: (error) => {
            console.log('Protected API status:', error.status);
            console.log('Protected API error:', error.error);
    }
  });
},
      // next: () => {
      //   this.successMessage = 'Login successful! Tokens stored.';
      //   console.log('Access token stored in localStorage.');
      // },
      // error: (error) => {
      //   this.errorMessage =
      //   error.error?.detail || 'Login failed. Check credentials or backend.';
      // }
    });
  }

}
