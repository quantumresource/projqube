from projqext.projectq.cengines._permutation_engine._linkedlist import DoubleLinkedList


def test_LinkedList():
	ll = DoubleLinkedList()
	assert(ll.count() == 0 and "count function returns wrong count for empty list")
	ll.push_back(3)	
	ll.push_front(1)	
	elem3 = ll.back
	ll.insert_before(elem3,2)

	count = 0
	current_ll = [1,2,3]
	for e in ll:
		assert(e.data == current_ll[count])
		count += 1

	assert(count == 3)

	count = 0
	current_ll = [3,2,1]
	for e in reversed(ll):
		assert(e.data == current_ll[count])
		count += 1

	ll.insert_after(ll.back,4)
	ll.insert_after(elem3,3.5)
	ll.insert_before(ll.head,0)

	assert(ll.remove_element(elem3.next) == 3.5)


	assert(ll.count() == 5)

	ll.swap_elements(ll.head.next,ll.head)
	ll.swap_elements(ll.back.prev.prev, ll.back)

	print("--")
	count = 0
	current_ll = [1,0,4,3,2]
	for e in ll:
		assert(e.data == current_ll[count])
		count += 1

	print("reversed")
	count=0
	for e in reversed(ll):
		assert(e.data == current_ll[4-count])
		count += 1

	ll.swap_elements(ll.head,ll.head.next)

	assert(ll.pop_front() == 0)
	assert(ll.pop_back() == 2)
	return



def test_swap_elements():
	ll = DoubleLinkedList()
	ll.push_front(2)
	ll.push_front(1)

	count = 0
	current_ll = [1,2]
	for e in ll:
		assert(e.data == current_ll[count])
		count += 1

	ll.swap_elements(ll.head, ll.back)

	print(ll.head.data)
	print(ll.back.data)

	count = 0
	current_ll = [2,1]
	for e in ll:
		print(e)
		assert(e.data == current_ll[count])
		count += 1
	return