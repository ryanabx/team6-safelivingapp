import { Component, ElementRef, Inject, Injectable, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { AppService } from './app.service';
import { AddrInputService } from './addr-input.service';
import { UserService } from './user.service';
import { throwError } from 'rxjs';

/*
@Injectable({
  providedIn: 'root'
})*/

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: []
})

export class AppComponent implements OnInit {
  title = 'tusafeliving';
  public inputAddr: any;
  public newpassword: string;
  public newuser: any;
  public user: any;

constructor(public _userService: UserService) {
  this.newpassword = '';
}
/*
  sendInput(value: string) {
    this.inputAddr = value;
    console.log(this.inputAddr);
    this.addrInputService.setAddr(this.inputAddr);
    this.router.navigateByUrl('/coord-list');
   }
*/
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

  login() {
    this._userService.login({'username': this.user.username, 'password': this.user.password});
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

  register() {
    this._userService.register(this.newuser.username, this.newuser.email, this.newuser.password).subscribe();
  }
}

