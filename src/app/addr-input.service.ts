import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AddrInputService {

  constructor() { }

  private addrInput: any;

  // called from another component to set the inputAddr
  // to be shared to other components
  setAddr(input: any) {
    this.addrInput = input;
  }

  // called from another component to receive the value
  // from addrInput
  getAddr() {
    return this.addrInput;
  }
}
