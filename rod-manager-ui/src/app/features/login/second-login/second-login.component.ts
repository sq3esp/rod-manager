import {Component, Inject} from '@angular/core';
import {AbstractControl, FormBuilder, FormGroup, ValidationErrors, ValidatorFn, Validators} from "@angular/forms";
import {NgxSpinnerService} from "ngx-spinner";
import {ForgetPasswordService} from "../../forget-password/forget-password.service";
import {MatSnackBar} from "@angular/material/snack-bar";
import {ActivatedRoute, Router} from "@angular/router";
import {ToastrService} from "ngx-toastr";
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";
import {GardenPlotWithLeaseholder} from "../../list-of-garden-plot/garden-plot";
import {Profile} from "../../Profile";
import {LoginUser} from "../../register/user.model";
import {AuthService} from "../../../core/auth/auth.service";
import {StorageService} from "../../../core/storage/storage.service";

@Component({
  selector: 'app-second-login',
  templateUrl: './second-login.component.html',
  styleUrls: ['./second-login.component.scss']
})
export class SecondLoginComponent {

  email: string = ''
  password: string = ''

  errorMessages = {
    code: [
      {type: 'required', message: 'Kod jest wymagany'},
    ]
  };

  codeForm: FormGroup;

  constructor(
    private spinner: NgxSpinnerService,
    private forgetPasswordService: ForgetPasswordService,
    private _snackBar: MatSnackBar,
    private router: Router,
    formBuilder: FormBuilder,
    private toastr: ToastrService,
    private route: ActivatedRoute,
    private authService: AuthService,
    private storageService: StorageService,
    public dialogRef: MatDialogRef<SecondLoginComponent>,
    @Inject(MAT_DIALOG_DATA) public data: {
      email: string,
      password: string,
    }
  ) {
    this.email = data.email;
    this.password = data.password;
    this.router = router;
    this.authService = authService;
    this.storageService = storageService;
    this.codeForm = formBuilder.group({
      code: ['', [Validators.required]],
    });
  }

  closeSecondDialog() {
    this.dialogRef.close();
  }

  validationErrors(controlName: string): any[] {
    let errors = []
    // @ts-ignore
    for (let error of this.errorMessages[controlName]) {
      if (this.codeForm.get(controlName)?.hasError(error.type)) {
        errors.push(error);
      }
    }
    return errors;
  }

  login(): void {
    let user = new LoginUser();
    user.email = this.email;
    user.password = this.password;
    this.spinner.show();
    this.authService.loginSecond(user,this.codeForm.get("code")?.value).subscribe({
      next: data => {
        this.toastr.success('Zalogowano!', 'Sukces');
        this.storageService.setTokens(data.access, data.refresh);
        this.storageService.setRoles(data.roles);
        this.spinner.hide();
        this.router.navigate(['home'])
        this.closeSecondDialog();
      },
      error: error => {
        this.toastr.error('Ups, nie udało się zalogowoać', 'Error');
        this.spinner.hide();
      }
    });
  }
}
