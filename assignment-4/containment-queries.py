from sys import argv
from csv import reader
from timeit import default_timer

class Data:
    """
    Data structure for transactions and queries.
    Contains an identifier and a list of objects.
    """

    def __init__(self, identifier, objects):
        self.id = identifier
        self.objects = set(objects)

def convert_to_int(string):
    string[0] = string[0][1:]
    string[-1] = string[-1][:-1]
    string = list(map(int, string))

    return string

def load_transactions(transactions_file):
    transactions = []
    with open(transactions_file, 'r') as tfile:
        csv = reader(tfile, delimiter=',')
        identifier = 0
        for line in csv:
            line = convert_to_int(line)
            transactions.append(Data(identifier, line))
            identifier += 1

    return transactions

def load_queries(queries_file):
    queries = []
    with open(queries_file, 'r') as qfile:
        csv = reader(qfile, delimiter=',')
        identifier = 0
        for line in csv:
            line = convert_to_int(line)
            queries.append(Data(identifier, line))
            identifier += 1

    return queries

# PART 1
def naive_method(transactions, queries, query_id):
    results = []
    if query_id == -1:
        for q in queries:
            for t in transactions:
                if q.objects.issubset(t.objects):
                    results.append(t.id)
    else:
        for t in transactions:
            if queries[query_id].objects.issubset(t.objects):
                results.append(t.id)

        return results

# PART 2
def convert_to_bitmap(identities):
    bitmap = 0
    for identity in identities:
        bitmap |= (1 << identity)

    return bitmap

def construct_sigfile(transactions):
    sigfile = []
    for t in transactions:
        bitmap = convert_to_bitmap([x for x in t.objects])
        sigfile.append(bitmap)

    return sigfile

def contains(sigfile, query):
    results = []
    for index, bitmap in enumerate(sigfile):

        if (query & bitmap) == query:
            results.append(index)

    return results

def export_sigfile(sigfile):
    with open("sigfile.txt", 'w') as out:
        for entry in sigfile:
            out.write("{}\n".format(entry))

def exact_signature_file_method(sigfile, queries, query_id):
    results = []
    if query_id == -1:
        for q in queries:
            query_bitmap = convert_to_bitmap([x for x in q.objects])
            results = contains(sigfile, query_bitmap)
    else:
        query_bitmap = convert_to_bitmap([x for x in queries[query_id].objects])
        results = contains(sigfile, query_bitmap)

        return results

#PART 3
def construct_bitslice(transactions):
    bitslice = {}
    for t in transactions:
        for obj in t.objects:
            if obj not in bitslice.keys():
                bitslice[obj] = (1 << t.id)
            else:
                bitslice[obj] += (1 << t.id)

    return bitslice

def export_bitslice(bitslice):
    with open("bitslice.txt", 'w') as out:
        for index in sorted(bitslice.keys()):
            out.write("{}: {}\n".format(index, bitslice[index]))

def decompress_bitslice(num):
    transaction_ids, index = [], 0
    while num > 0:
        if (num & 1) == 1:
            transaction_ids.append(index)
        num >>= 1
        index += 1
    return transaction_ids

def exact_bitslice_signature_file_method(bitslice, queries, query_id):
    results = []
    if query_id == -1:
        for q in queries:
            bitmap = -1
            for obj in q.objects:
                bitmap &= bitslice[obj]
            results = decompress_bitslice(bitmap)
    else:
        bitmap = -1
        for obj in queries[query_id].objects:
            bitmap &= bitslice[obj]
        results = decompress_bitslice(bitmap)

        return results

# PART 4
def construct_inverted_file(transactions):
    inverted_file = {}
    for t in transactions:
        for obj in t.objects:
            if obj not in inverted_file.keys():
                inverted_file[obj] = [t.id]
            else:
                inverted_file[obj].append(t.id)

    return inverted_file

def export_inverted_file(inverted_file):
    with open("invfile.txt", 'w') as out:
        for index in sorted(inverted_file.keys()):
            out.write("{}: {}\n".format(index, inverted_file[index]))

def inverted_file_method(inverted_file, queries, query_id):
    results = []
    if query_id == -1:
        for q in queries:
            results = set(inverted_file[next(iter(queries[query_id].objects))])
            for obj in q.objects:
                results &= set(inverted_file[obj])
    else:
        results = set(inverted_file[next(iter(queries[query_id].objects))])
        for obj in queries[query_id].objects:
            results &= set(inverted_file[obj])

        return results

def print_results(method_name, results, time):
    print("{} result:".format(method_name))
    print(results)
    print("{} computation time = {}".format(method_name, time))

def execute_method(transactions, queries, qnum, sigfile, bitslice, inverted_file, method):
    results = []
    start = default_timer()

    if method == 0:
        results = naive_method(transactions, queries, qnum)
        time = default_timer() - start
        if qnum != -1:
            print_results("Naive Method", results, time)
        else:
            print("Naive Method computation time = {}".format(time))
    elif method == 1:
        results = exact_signature_file_method(sigfile, queries, qnum)
        time = default_timer() - start
        if qnum != -1:
            print_results("Signature File", results, time)
        else:
            print("Signature File computation time = {}".format(time))
    elif method == 2:
        results = exact_bitslice_signature_file_method(bitslice, queries, qnum)
        time = default_timer() - start
        if qnum != -1:
            print_results("Bitsliced Signature File", results, time)
        else:
            print("Bitsliced Signature File computation time = {}".format(time))
    elif method == 3:
        results = inverted_file_method(inverted_file, queries, qnum)
        time = default_timer() - start
        if qnum != -1:
            print_results("Inverted File", results, time)
        else:
            print("Inverted File computation time = {}".format(time))
    elif method == -1:
        results = naive_method(transactions, queries, qnum)
        time = default_timer() - start
        if qnum != -1:
            print_results("Naive Method", results, time)
        else:
            print("Naive Method computation time = {}".format(time))

        start = default_timer()
        results = exact_signature_file_method(sigfile, queries, qnum)
        time = default_timer() - start
        if qnum != -1:
            print_results("Signature File", results, time)
        else:
            print("Signature File computation time = {}".format(time))

        start = default_timer()
        results = exact_bitslice_signature_file_method(bitslice, queries, qnum)
        time = default_timer() - start
        if qnum != -1:
            print_results("Bitsliced Signature File", results, time)
        else:
            print("Bitsliced Signature File computation time = {}".format(time))

        start = default_timer()
        results = inverted_file_method(inverted_file, queries, qnum)
        time = default_timer() - start
        if qnum != -1:
            print_results("Inverted File", results, time)
        else:
            print("Inverted File computation time = {}".format(time))
    else:
        print("Wrong input number!")

if __name__ == '__main__':
    # Load txt data to memory
    transactions = load_transactions(transactions_file = argv[1])
    queries = load_queries(queries_file = argv[2])

    sigfile = construct_sigfile(transactions)
    export_sigfile(sigfile)

    bitslice = construct_bitslice(transactions)
    export_bitslice(bitslice)

    inverted_file = construct_inverted_file(transactions)
    export_inverted_file(inverted_file)

    qnum, method = int(argv[3]), int(argv[4])

    execute_method(
        transactions, queries, qnum, sigfile, bitslice, inverted_file, method)
