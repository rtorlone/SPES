import { Component, OnInit, Input, Output , EventEmitter} from '@angular/core';

@Component({
  selector: 'app-pagination',
  templateUrl: './pagination.component.html',
  styleUrls: ['./pagination.component.css']
})
export class PaginationComponent implements OnInit {
// @ts-ignore
  @Input() page: number;
// @ts-ignore
  @Input() count: number;
// @ts-ignore
  @Input() perPage: number;
// @ts-ignore
  @Input() pagesToShow: number;
// @ts-ignore
  @Input() loading: boolean;
// @ts-ignore
  @Input() nome: string;

@Output() goPrev = new EventEmitter<boolean>();
@Output() goNext = new EventEmitter<boolean>();
@Output() goPage = new EventEmitter<number>();
  constructor() {
  }

  ngOnInit() {
  }

  onPrev(): void{
    this.goPrev.emit(true);
  }
  onNext(): void{
    this.goNext.emit(true);
  }
  onPage(n:number): void{
    this.goPage.emit(n);
  }
  totalPages() :number{
  return Math.ceil( this.count / this.perPage) || 0;
  }
  isLastPage() :boolean{
  return this.perPage* this.page >=this.count;}
  getPages(): number[]{
    const totalPages =this.totalPages();
    const thisPage= this.page ||1;
    const pagesToShow= this.pagesToShow || 9;
    const pages: number[]=[];
    pages.push(thisPage);

    for(let i=0;i < pagesToShow-1;i++){
      if(pages.length < pagesToShow)
         if(Math.min.apply(null,pages)> 1)
           pages.push(Math.min.apply(null,pages)-1);
           if(pages.length < pagesToShow )
            if(Math.max.apply(null,pages) <totalPages)
               pages.push(Math.max.apply(null, pages)+1);
    }
    pages.sort((a, b)=> a-b);
    return pages;}
  getMin(): number{
  return ((this.perPage *this.page)-this.perPage)+1;
  }
  getMax() :number{

    let max= this.perPage *this.page;
    if(max>this.count)
    max=this.count;

    return max;
  }
}

