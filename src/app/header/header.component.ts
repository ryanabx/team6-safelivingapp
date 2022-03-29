/*
Created By:
Last Edited By:
Date Created:
Date Last Edited:
Description:
*/


import { Component } from '@angular/core';
import { UserService } from '../user.service';

@Component({
    selector: 'app-header',
    templateUrl: './header.component.html',
    styleUrls: ['./header.component.css']
})

export class HeaderComponent {
    constructor(public _userService: UserService) {}
    
    logout() {
        this._userService.logout();
    }  
}