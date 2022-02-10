import { Component } from '@angular/core';
import { UserService } from '../user.service';

@Component({
    selector: 'app-footer',
    templateUrl: './footer.component.html',
    styleUrls: ['./footer.component.css']
})

export class FooterComponent {
    constructor(public _userService: UserService) {}

}