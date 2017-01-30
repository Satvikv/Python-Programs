def binary_search_func(nums_list,search_elem):
    sorting_an_array(nums_list,0,len(nums_list)-1);
def sorting_an_array(nums_list,left,right):

    if right > 1:
        mid=left+right/2
        sorting_an_array(nums_list,left,mid)
        sorting_an_array(nums_list,mid+1,right)
        merge_sort(nums_list,left,mid,right)
    return nums_list






def merge_sort(nums_list,left,mid,right):

    first_half_length=mid-left+1
    second_half_length=right-mid
    first_half=list()
    second_half=list()


    for i in range(first_half_length):
        first_half[i]=nums_list[i]
    for j in range(second_half_length):
        second_half=nums_list[j]
    i=0
    j=0
    k=0
    while i < first_half_length and j < second_half_length:
        if first_half[i] <= second_half[j]:
            nums_list[k]=first_half[i]
            i+=1
        else:
            nums_list[k]=second_half[j]
            j+=1
        k+=1

    while i<first_half_length:
        nums_list[k]=first_half[i]
        i+=1
        k+=1
    while j < second_half_length:
        nums_list[k]=second_half[j]
        j+=1
        k+=1






new_list=[2,5,7,8,2,4,6,7,8,34,12,46,875,67,45,4,2,146,7,58,434,232,5,6,773,4,63,23,42,53,45,36,36,4,6564]
print("index is ",binary_search_func(new_list,53))
