#include "mean_stacking.h"

void init_rand_matrix_ms(int* matrix, int width, int height){
    srand(0);
    for(int i = 0; i < width * height; i++){
        matrix[i] = rand()%10;
    }

}

void init_matrix_ms(int* matrix, int width, int height){
    for(int itr = 0; itr < width * height; itr++){
        matrix[itr] = 0;
    }
}

void mean_stack(int* result, int* next, int width, int height, int num_images){
    for(int itr = 0; itr < width * height; itr++){
        next[itr] = next[itr]/num_images;
    }
    for(int itr = 0; itr < width * height; itr++){
        result[itr] += next[itr];
    }
}

__global__ void initRandMatrixMs(int* matrix, int width, int height){
    int itr = threadIdx.x;
    matrix[itr] = clock()%10;
}

__global__ void initMatrixMs(int* matrix, int width, int height){
    int itr = threadIdx.x;
    matrix[itr] = 0;
}

__global__ void meanStack(int* result, int* next, int width, int height, int num_images){
    int itr = threadIdx.x;
    result[itr] += next[itr]/num_images;
}

int verified(){
    int array1[9] = {137, 432, 96, 12, 198, 323, 54, 2, 45};
    int array2[9] = {73, 109, 92, 129, 98, 363, 5, 23, 33};
    int result[9] = {104, 270, 94, 70, 148, 342, 29, 12, 38};
    int* test = (int*)malloc(sizeof(int)*9);

    int* d_array1;
    int* d_array2;
    int* d_result;

    cudaMalloc((void**)&d_array1,  sizeof(int) * 9);
    cudaMalloc((void**)&d_array2,  sizeof(int) * 9);
    cudaMalloc((void**)&d_result,  sizeof(int) * 9);

    cudaMemcpy(d_array1, array1, sizeof(int)*9, cudaMemcpyHostToDevice);
    cudaMemcpy(d_array2, array2, sizeof(int)*9, cudaMemcpyHostToDevice);
    
    initRandMatrixMs<<<9,9>>>(d_result, 3, 3);
    cudaMemcpy(test, d_result, sizeof(int)*9, cudaMemcpyHostToDevice);
    for(int itr = 0; itr < 9; itr++){
        printf("%d ", test[itr]);
    }
    printf("\n");
    initMatrixMs<<<9,9>>>(d_result, 3, 3);

    cudaMemcpy(test, d_result, sizeof(int)*9, cudaMemcpyHostToDevice);
    for(int itr = 0; itr < 9; itr++){
        printf("%d ", test[itr]);
        if(test[itr] != 0){
            printf("\n");
            return 0;
        }
    }
    printf("\n");

    meanStack<<<9,9>>>(d_result, d_array1, 3, 3, 2);
    meanStack<<<9,9>>>(d_result, d_array2, 3, 3, 2);
    cudaMemcpy(test, d_result, sizeof(int)*9, cudaMemcpyHostToDevice);

    for(int itr = 0; itr < 9; itr++){
        printf("%d ", test[itr]);
        if(test[itr] != result[itr]){
            printf("\n");
            return 0;
        }
    }
    printf("\n");

    cudaFree(d_array1);
    cudaFree(d_array2);
    cudaFree(result);

    return 1;
}

double mean_stack_timed_test(){
    struct timespec time_start;
    struct timespec time_end;

    struct timespec total_time_start;
    struct timespec total_time_end;

    int num_images = 100;
    int width = 5496;
    int height = 3672;
    int N = width*height;

    if(!verified()){
        printf("Verification Unsucessful\n");
        exit(1);
    }else{
        printf("Verification Sucessful\n");
    }

    srand(0);

    clock_gettime(CLOCK_REALTIME, &total_time_start);

    int* d_result;
    cudaMalloc((void**)&d_result,  sizeof(int) * width * height);
    initMatrixMs<<<N,N>>>(d_result, width, height);

    clock_gettime(CLOCK_REALTIME, &time_start);
    for(int itr = 0; itr < num_images; itr++){

        int* d_image;
        cudaMalloc((void**)&d_image,  sizeof(int) * width * height);
        initRandMatrixMs<<<N,N>>>(d_image, width, height);

        meanStack<<<N, N>>>(d_result, d_image, width, height, num_images);
        cudaFree(d_image);
    }
    clock_gettime(CLOCK_REALTIME, &time_end);

    cudaFree(d_result);

    clock_gettime(CLOCK_REALTIME, &total_time_end);
    printf("\nCUDA time: %lfs\n", (time_end.tv_sec - time_start.tv_sec) + ((double)(time_end.tv_nsec - time_start.tv_nsec)/1000000000));
    printf("\nTotal time: %lfs\n", (total_time_end.tv_sec - total_time_start.tv_sec) + ((double)(total_time_end.tv_nsec - total_time_start.tv_nsec)/1000000000));
    return (time_end.tv_sec - time_start.tv_sec) + ((double)(time_end.tv_nsec - time_start.tv_nsec)/1000000000);
}

// int main(){
//     mean_stack_timed_test();
//     return 0;
// }