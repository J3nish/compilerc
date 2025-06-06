#include<stdio.h>

int main(){
int a,b,sum;
printf("enter number 1:");
fflush(stdout);
scanf("%d",&a);
printf("enter number 2:");
fflush(stdout);
scanf("%d",&b);
sum = a+b;
printf("The sum of both number is %d",sum);
return 0;
}