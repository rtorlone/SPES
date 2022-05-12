import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UpdateDocComponent } from './update-doc.component';

describe('UpdateDocComponent', () => {
  let component: UpdateDocComponent;
  let fixture: ComponentFixture<UpdateDocComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UpdateDocComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UpdateDocComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
