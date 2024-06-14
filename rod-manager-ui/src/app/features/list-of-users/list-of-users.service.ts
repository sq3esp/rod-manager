import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Profile} from "../Profile";
import {Page} from "../../shared/paginator/page.model";
import {map, Observable, of} from "rxjs";
import {Role} from "../register/user.model";

@Injectable({
    providedIn: 'root'
})
export class ListOfUsersService {
    gardeneirsAPI ='api/gardeners/'
    constructor(private httpClient: HttpClient) {
    }

    getProfiles(index: number, size: number): Observable<Page<Profile>> {
        const url = `api/accounts/?page=${index}&page_size=${size}`;
        return this.httpClient.get<Page<Profile>>(url);
    }

    getAllProfiles(): Observable<Profile[]> {
        const url = `api/accounts/?page=${1}&page_size=${100000}`;
        return this.httpClient.get<Page<Profile>>(url).pipe(
            map((page: Page<Profile>) => page.results)
        );
    }

    getALLGardeiners(index: number, size: number): Observable<Page<Profile>> {
      const url = `${this.gardeneirsAPI}?page=${index}&page_size=${size}`;
      return this.httpClient.get<Page<Profile>>(url);
    }

    getALLGardeinersWithDebt(index: number, size: number): Observable<Page<Profile>> {
        const url = `${this.gardeneirsAPI}?page=${index}&page_size=${size}&payment_arrears=false`;
        return this.httpClient.get<Page<Profile>>(url);
    }

    getProfileById(id: string | null): Observable<Profile | undefined> {
        const url = `api/accounts/${id}/`;
        return this.httpClient.get<Profile>(url);
    }


    editProfile(profile: any,id: string | null) {
        const url = `api/accounts/${id}/`;
        console.log(profile);

        return this.httpClient.patch(url, profile);
    }

}

// .
// .
// .
// .
// .
// .
// .
// .
// .
// .
// .
// .
// .
// .
// .
// .
//
// ### GET request to retrieve profiles
//
// Retrieves a paginated list of profiles.
//
// #### Endpoint
//
// - Method: `GET`
// - URL: `https://localhost:1337/api/profiles`
// - Query Parameters:
//   - `page`: The page number to retrieve.
// - `size`: The number of profiles per page.
//
// #### Response
//
// The response body contains a paginated list of profiles.
//
//   ```typescript
// interface Profile {
//   profileId: string;
//   firstName: string;
//   lastName: string;
//   phoneNumber: string;
//   email: string;
//   accountStatus: Role[];
//   paymentAmount: number | null;
//   paymentDueDate: Date;
// }
//
// export enum Role {
//     ADMIN = 'ADMIN',
//     MANAGER = 'MANAGER',
//     GARDENER = 'GARDENER',
//     TECHNICAL_EMPLOYEE = 'TECHNICAL_EMPLOYEE',
//     NON_TECHNICAL_EMPLOYEE = 'NON_TECHNICAL_EMPLOYEE',
// }
//
// interface Page<T> {
//   count: number;
//   results: T[];
// }
// .
// .
// .
// .
// .
// .
// .
// .
// .
// .
// .
// .
// .
// .
// .
// .
// .
// ### GET request to fetch all profiles
//
// Retrieves all profiles available in the system.
//
// #### Endpoint
//
// - Method: `GET`
// - URL: `https://localhost:1337/api/all-profiles`
//
// #### Response
//
// The response body contains an array of profiles.
//
//   ```typescript
// interface Profile {
//   profileId: string;
//   firstName: string;
//   lastName: string;
//   phoneNumber: string;
//   email: string;
//   accountStatus: Role[];
//   paymentAmount: number | null;
//   paymentDueDate: Date;
// }
//
// export enum Role {
//   ADMIN = 'ADMIN',
//   MANAGER = 'Zarządca',
//   GARDENER = 'Działkowicz',
//   TECHNICAL_EMPLOYEE = 'pracownik_techniczny',
//   NON_TECHNICAL_EMPLOYEE = 'pracownik_nie_techniczny',
// }

