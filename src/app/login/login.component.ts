import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../user.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})

export class LoginComponent implements OnInit {
  title = 'tusafeliving';
  public inputAddr: any;
  public newpassword: string;
  public newuser: any;
  public user: any;

  constructor(private router: Router, public _userService: UserService) { 
    this.newpassword = '';}

  ngOnInit(): void {
    this.user = {
      username: '',
      password: ''
    };
    this.newuser = {
      username: '',
      email: '',
      password: ''
    };
  }

  sendToCreate(): void {
    this.router.navigate(['create']);
  }

  sendToBookmarks(): void {
    this.router.navigate(['bookmarks']);
  }

  login(username: string, password: string) {
    this.user.username = username;
    this.user.password = password;
    this._userService.login({'username': this.user.username, 'password': this.user.password});
    setTimeout(() => {
      if(this._userService.username != null)
      {
       this.sendToBookmarks();
      }
    }, 1500)
  }
 
  refreshToken() {
    this._userService.refreshToken();
  }
 
  logout() {
    this._userService.logout();
  }

  changePassword(newpassword: string) {
    this._userService.changePassword(this.user.username, this.user.password, newpassword).subscribe();
  }
}