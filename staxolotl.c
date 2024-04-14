// Reference
// https://www.geeksforgeeks.org/c-program-list-files-sub-directories-directory/

#include <stdio.h>
#include <dirent.h>
#include <string.h>
#include "fitsio.h"

struct image{
    int* data;
    int height;
    int width;
};

void image_init(struct image* init){
    init->data = NULL;
    init->height = 0;
    init->width = 0;
}

int load_image(){
    return 0;
}

int save_image(){
    return 0;
}

void mean_stack(int* result, int* next, int width, int height, int num_images){
    for(int itr = 0; itr < width * height; itr++){
        result[itr] += next[itr]/num_images;
    }
}



int main(int argc, char* argv[]){

    struct image image;
    image_init(&image);

    struct dirent* dir;

    DIR* folder_dir;
    if(argc > 1){
        folder_dir = opendir(argv[1]);
    }else{
        folder_dir = opendir("./moon_test/");
    }

    if(folder_dir == NULL){
        printf("No directory available");
        return 0;
    }

    while((dir = readdir(folder_dir)) != NULL){
        if(strncmp(dir->d_name, ".", 1) != 0 && strncmp(dir->d_name, "..", 2) != 0){

            char path[1024];
            if(argc > 1){
                strcpy(path, argv[1]);
            }else{
                strcpy(path, "./moon_test/");
            }
            strcat(path, dir->d_name);

            printf("%s\n", path);

            fitsfile* input_fptr;

            int status = 0,  nkeys;
            int bitpix = 0;

            int naxis[2] = {0,0};
            long naxes[2] = {0,0};

            fits_open_file(&input_fptr, path, READONLY, &status);
            fits_get_hdrspace(input_fptr, &nkeys, NULL, &status);
            fits_get_img_param(input_fptr, 2, &bitpix, naxis, naxes, &status);
            printf("Type: %d\n", bitpix);
            printf("Dimensions: %ld, %ld\n", naxes[0], naxes[1]);
            printf("Data:\n");

            long fpixel[2] = {1,1};
            int16_t array[naxis[0]*naxes[1]]
            fits_read_pix(&input_fptr, bitpix, &fpixel, (naxis[0]*naxes[1]), NULL, ,,&status);

            printf("%d", );
            

        }
    }

    closedir(folder_dir);

    return 0;
}