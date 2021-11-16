import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
 
@Injectable()
export class UserService {
 
  // http options used for making API calls
  private httpOptions: any;
 
  // the actual JWT token
  public token: string | null;
 
  // the token expiration date
  public token_expires: Date | null;
 
  // the username of the logged in user
  public username: string | null;
 
  // error messages received from the login attempt
  public errors: any = [];
 
  constructor(private http: HttpClient) {
    this.httpOptions = {
      headers: new HttpHeaders({'Content-Type': 'application/json'})
    };
    this.token = null;
    this.token_expires = null;
    this.username = null;
  }
 
  // Uses http.post() to get an auth token from djangorestframework-jwt endpoint
  public login(user: any) {
    this.http.post('http://localhost:8000/api-token-auth/', JSON.stringify(user), this.httpOptions).subscribe(
      (data: any) => {
        this.updateData(data['token']);
      },
      err => {
        this.errors = err['error'];
      }
    );
  }
 
  // Refreshes the JWT token, to extend the time the user is logged in
  public refreshToken() {
    this.http.post('http://localhost:8000/api-token-refresh/', JSON.stringify({token: this.token}), this.httpOptions).subscribe(
      (data: any) => {
        this.updateData(data['token']);
      },
      err => {
        this.errors = err['error'];
      }
    );
  }

  public changePassword(username: string, password: string, newpassword: string) {
    return this.http.get("http://localhost:8000/user/change_password/" + username + "/" + password + "/" + newpassword + "/");
  }

  public register(username: string, email:string, password: string) {
    return this.http.get("http://localhost:8000/user/new_user/" + username + "/" + email + "/" + password + "/");
  }
 
  public logout() {
    this.token = null;
    this.token_expires = null;
    this.username = null;
  }
 
  private updateData(token: string) {
    this.token = token;
    this.errors = [];
 
    // decode the token to read the username and expiration timestamp
    const token_parts = this.token.split(/\./);
    const token_decoded = JSON.parse(window.atob(token_parts[1]));
    this.token_expires = new Date(token_decoded.exp * 1000);
    this.username = token_decoded.username;
    console.log(token_decoded);
  }
}