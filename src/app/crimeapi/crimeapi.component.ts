import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { analyzeAndValidateNgModules } from '@angular/compiler';

@Component({
  selector: 'app-crimeapi',
  templateUrl: './crimeapi.component.html',
  styleUrls: ['./crimeapi.component.css']
})
export class CrimeapiComponent implements OnInit {

  url = 'https://api.usa.gov/crime/fbi/sapi//api/summarized/agencies/FL0500500/offenses/2019/2020?api_key=nHym62MTPDELS0XgtAZLLw0fL3jNWoNvsY2kn315';
  items: any = [];
  /*
    nationalCrimeData stores a array of integers whose indicies correspond
    to the offense in the order presented for national 2020 data, 
    0 - property crime
    1 - violent crime
    2 - robbery
    3 - rape
    4 - motor vehicle theft
    5 - larceny
    6 - human trafficking
    7 - homicide
    8 - burglary
    9 - arson
    10 - aggravated assault
    rape and rape-legacy are combined into one number, since rape is rape.
  
  nationalCrimeData = [3424591, 640836, 102677, 68258, 426799, 2453533, 579, 10440, 522426, 21833, 459461];
  */
  // actual statistics from API call for a given location
  propertyCrime: number = 0;
  violentCrime: number = 0;
  robbery: number = 0;
  rape: number = 0;
  mvTheft: number = 0;
  larceny: number = 0;
  humanTraff: number = 0;
  homicide: number = 0;
  burglary: number = 0;
  arson: number = 0;
  aggrAss: number = 0;

  /*
  // percentages with respect to the API information and national data
  pcPercent: number = (this.propertyCrime / this.nationalCrimeData[0]) * 100
  vcPercent: number = (this.violentCrime / this.nationalCrimeData[1]) * 100
  robPercent: number = (this.robbery / this.nationalCrimeData[2]) * 100
  rapePercent: number = (this.rape / this.nationalCrimeData[3]) * 100
  mvtPercent: number = (this.mvTheft / this.nationalCrimeData[4]) * 100
  larcPercent: number = (this.larceny / this.nationalCrimeData[5]) * 100
  htPercent: number = (this.humanTraff / this.nationalCrimeData[6]) * 100
  homiPercent: number = (this.homicide / this.nationalCrimeData[7]) * 100
  burgPercent: number = (this.burglary / this.nationalCrimeData[8]) * 100
  arsonPercent: number = (this.arson / this.nationalCrimeData[9]) * 100
  aaPercent: number = (this.aggrAss / this.nationalCrimeData[10]) * 100
  */
 
  keynames = [];
  file: any;
  ori: string;
  fromstr: string;
  tostr: string;
  from: number;
  to: number;
  returnedstuff;
  specificcrimedata: object;


  constructor(private http: HttpClient, private route: ActivatedRoute, private router: Router) {
    this.returnedstuff = new Object;
    this.specificcrimedata = new Object;
    this.ori = '';
    this.from = 0;
    this.to = 0;
    this.fromstr = '2020';
    this.tostr = '2020';


    this.route.queryParams
    .subscribe(params => {
      this.ori = params['ori'];
      /* ---Removing Option to search over multiple years, End-user mostly concerned with recent data
      this.fromstr = params['from'];
      this.from = this.fromstr ? (parseInt(params['from']) ? parseInt(params['from']) : new Date().getFullYear() - 5) : new Date().getFullYear() - 5;
      this.tostr = params['to'];
      this.to = this.tostr ? (parseInt(params['to']) ? parseInt(params['to']) : new Date().getFullYear()) : new Date().getFullYear();
      
      if(params['from'] != parseInt(params['from']) || params['to'] != parseInt(params['to']))
      {
        this.router.navigate(['crimeapi'], {queryParams: {ori: this.ori}}).then(()=>{window.location.reload()});
      }
      */
      this.router.navigate(['crimeapi'], {queryParams: {ori: this.ori}});//.then(()=>{window.location.reload()});
      /*
      if(this.from > this.to)
      {
        var temp = this.to;
        this.to = this.from;
        this.from = temp;
        this.router.navigate(['crimeapi'], {queryParams: {ori: this.ori}}).then(()=>{window.location.reload()});
      }*/
    });

    this.url = 'https://api.usa.gov/crime/fbi/sapi/api/summarized/agencies/'
    this.url += this.ori
    this.url += '/offenses/'
    this.url += this.fromstr
    this.url += '/'
    this.url += this.tostr
    this.url += '?api_key=nHym62MTPDELS0XgtAZLLw0fL3jNWoNvsY2kn315';

    this.http.get(this.url).toPromise().then(data =>{
      console.log(data);
      this.file = data
      this.items = this.file.results
      console.log(this.items);
      
      for (let i = 0; i < this.items.length; i++){
        if (this.items[i].offense == "property-crime"){
          this.propertyCrime += this.items[i].actual
        }
        else if (this.items[i].offense == "violent-crime"){
          this.violentCrime += this.items[i].actual
        }
        else if (this.items[i].offense == "robbery"){
          this.robbery += this.items[i].actual
        }
        else if (this.items[i].offense == "rape-legacy" || this.items[i].offense == "rape"){
          this.rape += this.items[i].actual
        }
        else if (this.items[i].offense == "motor-vehicle-theft"){
          this.mvTheft += this.items[i].actual
        }
        else if (this.items[i].offense == "larceny"){
          this.larceny += this.items[i].actual
        }
        else if (this.items[i].offense == "human-trafficing"){
          this.humanTraff += this.items[i].actual
        }
        else if (this.items[i].offense == "homicide"){
          this.homicide += this.items[i].actual
        }
        else if (this.items[i].offense == "burglary"){
          this.burglary += this.items[i].actual
        }
        else if (this.items[i].offense == "arson"){
          this.arson += this.items[i].actual
        }
        else if (this.items[i].offense == "aggravated-assault"){
          this.aggrAss += this.items[i].actual
        }
      }

      /*
      for (let key in data){
        if(data.hasOwnProperty(key)){
          var str : string;
          str = '';
          var str2 : string;
          str2 = JSON.stringify(key);
          str += str2;
          str += ": ";
          str += JSON.stringify(data[key as never]);
          this.items.push(str as never);
        }
      }*/
    });
   }

  ngOnInit(): void {
    
  }

}
function zillowRoute() {
  throw new Error('Function not implemented.');
}

