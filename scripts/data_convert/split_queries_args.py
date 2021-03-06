#
#  Copyright 2014+ Carnegie Mellon University
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
def add_basic_query_split_args(parser):
    parser.add_argument('--seed',
                        metavar='random seed',
                        help='random seed',
                        type=int, default=0)
    parser.add_argument('--partitions_names',
                        metavar='names of partitions to split at',
                        help='names of partitions to split at separated by comma',
                        required=True,
                        type=str)
    parser.add_argument('--partitions_sizes',
                        metavar='sizes of partitions to split at',
                        help="sizes (in queries) of partitions to split at separated by comma (one of the values can be missing, "
                             "in that case all left queries go to that partition)",
                        required=True,
                        type=str)


class QuerySplitArgumentsBase:
    def __init__(self, raw_args):
        self.raw_args = raw_args

    @property
    def src_dir(self):
        return self.raw_args.src_dir

    @property
    def dst_dir(self):
        return self.raw_args.dst_dir
    
    @property
    def seed(self):
        return self.raw_args.seed
     
    @property    
    def partitions_names(self):
        return self.raw_args.partitions_names.split(',')
    
    def partitions_sizes(self, queries_count):
        raw_values = []
        for value in self.raw_args.partitions_sizes.split(','):
            if value == '':
                raw_values.append(-1)
            else:
                raw_values.append(int(value))
        nondefined_count = 0
        defined_sum = 0
        for value in raw_values:
            if value != -1:
                if value <= 0:
                    raise Exception('One query list is empty!')
                if value >= queries_count:
                    raise Exception(f'A partition is too big, the total number of queries is only: {queries_count}')
                defined_sum += value
            else:
                nondefined_count += 1

        if nondefined_count == 0 and defined_sum == queries_count:
            return raw_values
        elif nondefined_count == 1 and defined_sum < queries_count:
            raw_values[raw_values.index(-1)] = queries_count - defined_sum
            return raw_values
        else:
            raise ValueError("invalid --partitions_sizes argument")
