/*
Created By:
Last Edited By:
Date Created:
Date Last Edited:
Description:
*/


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

  invalidLogin = false;
  lowercaseError = false;
  uppercaseError = false;
  numberError = false;
  symbolError = false;
  lengthError = false;
  usernameError = false;

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
    this._userService.register(this.newuser.email, this.newuser.username, this.newuser.password).subscribe(
      (data: any) => {
        this.lengthError = data.length_error;
        this.symbolError = data.symbol_error;
        this.lowercaseError = data.lowercase_error;
        this.uppercaseError = data.uppercase_error;
        this.invalidLogin = data.check_result;
        this.numberError = data.number_error;
        this.usernameError = data.username_error;
        
        this.invalidLogin = !this.invalidLogin;
        if (!this.invalidLogin){
          setTimeout(() => {
            this.sendToLogin();
          }, 1500);
        }
      }
    );
    
    
  }
}
