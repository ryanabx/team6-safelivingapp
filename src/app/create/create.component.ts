import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../user.service';

@Component({
  selector: 'app-create',
  templateUrl: './create.component.html',
  styleUrls: ['./create.component.css']
})
export class CreateComponent implements OnInit {
  public newuser: any;

  constructor(private router: Router, public _userService: UserService) { }

  ngOnInit(): void {
    this.newuser = {
      username: '',
      email: '',
      password: ''
    };
  }

  sendToLogin(): void {
    this.router.navigate(['login'])
  }

  register(email: string, username: string, password: string) {
    this.newuser.email = email;
    this.newuser.username = username;
    this.newuser.password = password;
    this._userService.register(this.newuser.email, this.newuser.username, this.newuser.password).subscribe();
    setTimeout(() => {
      this.sendToLogin();
    }, 1500);
  }
}
