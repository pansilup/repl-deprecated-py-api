#author : pansilup
#date   : 07-03-2022
#project: is706-finding missing python APIs from release notes

import os
import csv

def extract_data2(substr, flines):
  results = []
  line_no = 0
  for line in flines:
        substr_count = 0
        line_result = []
        line_result.append(line_no)
        line_result.append(substr_count)
        index = 0                   # current index: character being compared
        #prev = 0                    # previous index: last character compared
        while index < len(line):    # While index has not exceeded string length,
              index = line.lower().find(substr.lower(), index)  # set index to first occurrence of substr
              if index == -1:           # If nothing
                break                   
              line_result.append(index)
              substr_count += 1
              #prev = index + len(substr)# remember this position for next loop.
              index += len(substr)      # increment the index by the length of substr.
        line_result[1] = substr_count
        line_no += 1
        if substr_count > 0:
          results.append(line_result)

  return results #list{..., [line_no, substr_count, substr_loc_1,...substr_loc_n], ...}
#--------------------------------------------------------------------------------------

def extract_data(substr, flines):
    results = []
    line_no = 0
    for line in flines:
        index = line.lower().find(substr.lower())  # set index to first occurrence of substr
        if index != -1: 
            results.append(line_no)
        line_no = line_no + 1
    #if(len(results)) > 0:
    #    print("res",results)
    return results
#--------------------------------------------------------------------------------------
    
def split_api_name(m_api):
  words = m_api.split('.')
  l = len(words)
  variants = []
  i = 0
  prev = m_api
  while i < l-1:
      prev = prev[len(words[i])+1:]
      variants.append(prev)
      i += 1
  #print(variants)
  return variants
#--------------------------------------------------------------------------------------

def get_possible_variants(lib, m_api):
  p_var = []
  p_var.append(m_api)
  case_1 = "numpy"
  if lib.lower() == case_1:
        tmp = "np" + m_api[5:len(m_api)]
        p_var.append(tmp)
        
  return p_var
#--------------------------------------------------------------------------------------

def search_api(lib, api, fnames):
  s_results = []
  for filename in fnames:
        #print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%", filename)
        tlines = []
        if len(lib) > 0:
              filename = "dataRST/"+lib+"/"+filename
        else:
              filename = fnames[0]  #for testing with test files
              #print(filename)
        with open(filename, "rt", encoding="utf8") as myfile:
              for thisline in myfile:             
                    if thisline[0] != '\n' and thisline[0] != '\r': 
                          tlines.append(thisline.rstrip('\n'))
        myfile.close()
        #tline_count = len(tlines)
        #print(tline_count)
        #print(tlines)
        
        hits_in_file = extract_data(api, tlines)
        t_no_lines = len(tlines)
        t_s_results = []
        if len(hits_in_file) > 0:
              #print("hits",hits_in_file)
              t_s_results.append(filename)
              #print("\napi match in \t:", filename)
              for linehit in hits_in_file:
                    #print("hit :", linehit)
                    data = tlines[linehit]
                    i = linehit + 1
                    #print(linehit,i,t_no_lines, len(tlines))
                    while i < linehit + 5 and i < t_no_lines:
                        data = data + ' ' + tlines[i]
                        #print(i)
                        #print("\ndata", data)
                        i = i + 1
                    t_s_results.append(data)
                    #print("at line ", linehit, "\t:", tlines[linehit)
              #print(t_s_results)
              s_results.append(t_s_results)
  #print(s_results)
  return s_results
#--------------------------------------------------------------------------------------

def get_substr_locs(s_line, val):
    #print(s_line)
    index = 0
    locs = []                  
    while index < len(s_line):    
        index = s_line.lower().find(val.lower(), index)  # set index to first occurrence of substr
        if index == -1:           # If nothing
            break
        locs.append(index)
        index += len(val)      # increment the index by the length of sstr.
    #print("locs", locs)
    return locs
#--------------------------------------------------------------------------------------

def takeSecond(elem):
    return elem[1]
#--------------------------------------------------------------------------------------

def fetch_string(s_line, a_boundary, delim):
    new_api = []
    start = s_line.lower().find(delim.lower(), a_boundary[0])  # set index to first occurrence of substr
    if start > 0:           # If hit 
        end = s_line.lower().find(delim.lower(), start+len(delim))
        if a_boundary[1] == 'e' and end > start and end < len(s_line):
            new_api = s_line[start+len(delim):end]
        elif end > start and end < a_boundary[1]:
            new_api = s_line[start+len(delim):end]
            #print("new api : ", new_api)
    if new_api:
        if 'https' in new_api or '#' in new_api or '/' in new_api or '()' in new_api:
            new_api = []
            
    return new_api
#--------------------------------------------------------------------------------------

def check_if_real_hit(a_boundary, s_line):
    possible_api = []
    if a_boundary:
       possible_api = fetch_string(s_line, a_boundary, "`") #new api inside `` ``
       if(possible_api):
           return possible_api,1
       else:
           possible_api = fetch_string(s_line, a_boundary, "``") #new api inside ` `  
           if(possible_api):
               return possible_api,1
    return possible_api, 0

#--------------------------------------------------------------------------------------
def valid_key_idx(key_idxs):
    tmp = []
    
    return tmp
def extract_replacement(s_line, d_api):
    
    sdict = {}
    sdict['0'] = d_api
    sdict['1'] = 'removed'
    sdict['2'] = 'replaced' #
    sdict['3'] = 'deprecat'
    sdict['4'] = 'use'
    sdict['5'] = 'instead'
    sdict['6'] = 'alias' #
    sdict['7'] = 'in favor of' #
    sdict['8'] = 'equivalent' #
    sdict['9'] = 'used instead'
    sdict['10']= 'better'
    sdict['11']= 'replace'
    sdict['12']= 'with'
    sdict['13']= 'available'
    sdict['14']= 'expire'
    sdict['15']= 'old'
    sdict['16']= 'renamed'
    sdict['17']= 'superceded by'
    
    #old dep/remo 'equivalent' new
    #old dep/rem  new 'be used instead'
    
    n_api = []
    key_idxs = [] # { [k0_loc1,k0_loc2,...], [k1_loc1,k1_loc2,...], []}
    i = 0
    for key in sdict:
        ans = get_substr_locs(s_line, sdict[key])
        if ans:
            for idx in ans:
                tmp = (key, idx)
                key_idxs.append(tmp)
        i += 1
    #print(key_idxs)
    key_idxs.sort(key=takeSecond)
    print(key_idxs)
                
    #pattern 1: 0-1-2 >> '0-old_api' ... 1-removed ... 2-replaced by ``new_api``
    print("checking for pattern 1 ...")
    pattern = ['0', '1', '2']
    ph = [0, 0, 0]
    a_boundary = []
    got_it = 0
    s_l = 0
    for p in pattern:
        #print("p",p)
        l = 0
        for s in key_idxs[s_l:]:
            l += 1
            #print("key_idxs[:]",key_idxs[s_l:])
            if ph[0] == 0 and s[0] == p:
                ph[0] = 1
                s_l = l
                break
            elif ph[0] == 1 and ph[1] == 0 and s[0] == p:
                ph[1] = 1
                s_l = s_l + l
                break
            elif ph[1] == 1 and ph[2] == 0 and s[0] == p:
                ph[2] = 1
                a_boundary = [s[1], 'e']
                got_it = 1
                #print(a_boundary)
                break
    possible_api, got_it  = check_if_real_hit(a_boundary, s_line)

    #pattern 1: 0-1-2 >> '0-old_api' ... 3-deprecated ... 2-replaced by ``new_api``
    print("checking for pattern 2 ...")
    pattern = ['0', '3', '2']
    ph = [0, 0, 0]
    a_boundary = []
    got_it = 0
    s_l = 0
    for p in pattern:
        #print("p",p)
        l = 0
        for s in key_idxs[s_l:]:
            l += 1
            #print("key_idxs[:]",key_idxs[s_l:])
            if ph[0] == 0 and s[0] == p:
                ph[0] = 1
                s_l = l
                break
            elif ph[0] == 1 and ph[1] == 0 and s[0] == p:
                ph[1] = 1
                s_l = s_l + l
                break
            elif ph[1] == 1 and ph[2] == 0 and s[0] == p:
                ph[2] = 1
                a_boundary = [s[1], 'e']
                got_it = 1
                #print(a_boundary)
                break
    possible_api, got_it  = check_if_real_hit(a_boundary, s_line)


    if got_it == 0:
        #pattern 2: 0-14-4-5 >> '0-old_api' ... 14-expire ... 4-use ``new_api`` 5-instead
        print("checking for pattern 3 ...")
        pattern = ['0', '14', '4', '5']
        ph = [0, 0, 0, 0]
        a_boundary = []
        s_l = 0
        for p in pattern:
            #print("p",p)
            l = 0
            for s in key_idxs[s_l:]:
                l += 1
                #print("key_idxs[:]",key_idxs[s_l:])
                if ph[0] == 0 and s[0] == p:
                    ph[0] = 1
                    s_l = l
                    break
                elif ph[0] == 1 and ph[1] == 0 and s[0] == p:
                    ph[1] = 1
                    s_l = s_l + l
                    break
                elif ph[1] == 1 and ph[2] == 0 and s[0] == p:
                    ph[2] = 1
                    st = s[1]
                    #print("st", st)
                    s_l = s_l + l
                    break
                elif ph[2] == 1 and ph[3] == 0 and s[0] == p:
                    ph[3] == 1
                    a_boundary = [st, s[1]]
                    got_it = 1
                    #print("b",a_boundary)
                    break
        possible_api, got_it  = check_if_real_hit(a_boundary, s_line)
        
    if got_it == 0:
        #pattern 2: 0-3-4-5 >> '0-old_api' ... 3-deprecat ... 4-use ``new_api`` 5-instead
        print("checking for pattern 4 ...")
        pattern = ['0', '3', '4', '5']
        ph = [0, 0, 0, 0]
        a_boundary = []
        s_l = 0
        for p in pattern:
            #print("p",p)
            l = 0
            for s in key_idxs[s_l:]:
                l += 1
                #print("key_idxs[:]",key_idxs[s_l:])
                if ph[0] == 0 and s[0] == p:
                    ph[0] = 1
                    s_l = l
                    break
                elif ph[0] == 1 and ph[1] == 0 and s[0] == p:
                    ph[1] = 1
                    s_l = s_l + l
                    break
                elif ph[1] == 1 and ph[2] == 0 and s[0] == p:
                    ph[2] = 1
                    st = s[1]
                    #print("st", st)
                    s_l = s_l + l
                    break
                elif ph[2] == 1 and ph[3] == 0 and s[0] == p:
                    ph[3] == 1
                    a_boundary = [st, s[1]]
                    got_it = 1
                    #print("b",a_boundary)
                    break
        possible_api, got_it  = check_if_real_hit(a_boundary, s_line)

    if got_it == 0:
    #pattern 3: 0-3-6 >> '0-old_api' ... 3-deprecate ... 6-alias ``new_api``
        print("checking for pattern 5 ...")
        pattern = ['0', '3', '6']
        ph = [0, 0, 0]
        a_boundary = []
        got_it = 0
        s_l = 0
        for p in pattern:
            #print("p",p)
            l = 0
            for s in key_idxs[s_l:]:
                l += 1
                #print("key_idxs[:]",key_idxs[s_l:])
                if ph[0] == 0 and s[0] == p:
                    ph[0] = 1
                    s_l = l
                    break
                elif ph[0] == 1 and ph[1] == 0 and s[0] == p:
                    ph[1] = 1
                    s_l = s_l + l
                    break
                elif ph[1] == 1 and ph[2] == 0 and s[0] == p:
                    ph[2] = 1
                    a_boundary = [s[1], 'e']
                    got_it = 1
                    #print(a_boundary)
                    break
        possible_api, got_it  = check_if_real_hit(a_boundary, s_line)

    if got_it == 0:
    #pattern 4: 0-3-7 >> '0-old_api' ... 3-deprecate ... 6-in favor of ``new_api``
        print("checking for pattern 6 ...")
        pattern = ['0', '3', '7']
        ph = [0, 0, 0]
        a_boundary = []
        got_it = 0
        s_l = 0
        for p in pattern:
            #print("p",p)
            l = 0
            for s in key_idxs[s_l:]:
                l += 1
                #print("key_idxs[:]",key_idxs[s_l:])
                if ph[0] == 0 and s[0] == p:
                    ph[0] = 1
                    s_l = l
                    break
                elif ph[0] == 1 and ph[1] == 0 and s[0] == p:
                    ph[1] = 1
                    s_l = s_l + l
                    break
                elif ph[1] == 1 and ph[2] == 0 and s[0] == p:
                    ph[2] = 1
                    a_boundary = [s[1], 'e']
                    got_it = 1
                    #print(a_boundary)
                    break
        possible_api, got_it  = check_if_real_hit(a_boundary, s_line)

    if got_it == 0:
    #pattern 5: 0-3-7 >> '0-old_api' ... 3-deprecate ...  ``new_api`` 8-equivalent
        print("checking for pattern 7 ...")
        pattern = ['0', '3', '8']
        ph = [0, 0, 0]
        a_boundary = []
        got_it = 0
        s_l = 0
        for p in pattern:
            #print("p",p)
            l = 0
            for s in key_idxs[s_l:]:
                l += 1
                #print("key_idxs[:]",key_idxs[s_l:])
                if ph[0] == 0 and s[0] == p:
                    ph[0] = 1
                    s_l = l
                    break
                elif ph[0] == 1 and ph[1] == 0 and s[0] == p:
                    ph[1] = 1
                    st = s[1]
                    s_l = s_l + l
                    break
                elif ph[1] == 1 and ph[2] == 0 and s[0] == p:
                    ph[2] = 1
                    a_boundary = [st, s[1]]
                    got_it = 1
                    #print(a_boundary)
                    break
        possible_api, got_it  = check_if_real_hit(a_boundary, s_line)


    if got_it == 0:
    #pattern 5: 0-3-7 >> '0-old_api' ... 3-deprecate ... 8-equivalent ``new_api``
        print("checking for pattern 8 ...")
        pattern = ['0', '3', '8']
        ph = [0, 0, 0]
        a_boundary = []
        got_it = 0
        s_l = 0
        for p in pattern:
            #print("p",p)
            l = 0
            for s in key_idxs[s_l:]:
                l += 1
                #print("key_idxs[:]",key_idxs[s_l:])
                if ph[0] == 0 and s[0] == p:
                    ph[0] = 1
                    s_l = l
                    break
                elif ph[0] == 1 and ph[1] == 0 and s[0] == p:
                    ph[1] = 1
                    s_l = s_l + l
                    break
                elif ph[1] == 1 and ph[2] == 0 and s[0] == p:
                    ph[2] = 1
                    a_boundary = [s[1], 'e']
                    got_it = 1
                    #print(a_boundary)
                    break
        possible_api, got_it  = check_if_real_hit(a_boundary, s_line)


    if got_it == 0:
            #pattern 6: 0-1-4-5 >> '0-old_api' ... 1-removed ... 4-use ``new_api`` 5-instead
            print("checking for pattern 9 ...")
            pattern = ['0', '1', '4', '5']
            ph = [0, 0, 0, 0]
            a_boundary = []
            s_l = 0
            for p in pattern:
                #print("p",p)
                l = 0
                for s in key_idxs[s_l:]:
                    l += 1
                    #print("key_idxs[:]",key_idxs[s_l:])
                    if ph[0] == 0 and s[0] == p:
                        ph[0] = 1
                        s_l = l
                        break
                    elif ph[0] == 1 and ph[1] == 0 and s[0] == p:
                        ph[1] = 1
                        s_l = s_l + l
                        break
                    elif ph[1] == 1 and ph[2] == 0 and s[0] == p:
                        ph[2] = 1
                        st = s[1]
                        #print("st", st)
                        s_l = s_l + l
                        break
                    elif ph[2] == 1 and ph[3] == 0 and s[0] == p:
                        ph[3] == 1
                        a_boundary = [st, s[1]]
                        got_it = 1
                        #print("b",a_boundary)
                        break
            possible_api, got_it  = check_if_real_hit(a_boundary, s_line)

    if got_it == 0:
        #pattern 7: 0-3-8 >> '0-old_api' ... 3-deprecat ``new_api`` 8-equivalent
        print("checking for pattern 10 ...")
        pattern = ['0', '3', '8']
        ph = [0, 0, 0]
        a_boundary = []
        s_l = 0
        for p in pattern:
            #print("p",p)
            l = 0
            for s in key_idxs[s_l:]:
                l += 1
                #print("key_idxs[:]",key_idxs[s_l:])
                if ph[0] == 0 and s[0] == p:
                    ph[0] = 1
                    s_l = l
                    break
                elif ph[0] == 1 and ph[1] == 0 and s[0] == p:
                    ph[1] = 1
                    st = s[1]
                    s_l = s_l + l
                    break
                elif ph[1] == 1 and ph[2] == 0 and s[0] == p:
                    ph[2] = 1
                    a_boundary = [st, s[1]]
                    got_it = 1
                    break
        possible_api, got_it  = check_if_real_hit(a_boundary, s_line)
        
    if got_it == 0:
        #pattern 7: 0-3-9 >> '0-old_api' ... 3-deprecat ``new_api`` 9-used instead
        print("checking for pattern 11 ...")
        pattern = ['0', '3', '9']
        ph = [0, 0, 0]
        a_boundary = []
        s_l = 0
        for p in pattern:
            #print("p",p)
            l = 0
            for s in key_idxs[s_l:]:
                l += 1
                #print("key_idxs[:]",key_idxs[s_l:])
                if ph[0] == 0 and s[0] == p:
                    ph[0] = 1
                    s_l = l
                    break
                elif ph[0] == 1 and ph[1] == 0 and s[0] == p:
                    ph[1] = 1
                    st = s[1]
                    s_l = s_l + l
                    break
                elif ph[1] == 1 and ph[2] == 0 and s[0] == p:
                    ph[2] = 1
                    a_boundary = [st, s[1]]
                    got_it = 1
                    break
        possible_api, got_it  = check_if_real_hit(a_boundary, s_line)
    
    if got_it == 0:
        #pattern 2: 0-3-4 >> '0-old_api' ... 3-deprecat ... 4-use ``new_api``
        print("checking for pattern 12 ...")
        pattern = ['0', '3', '4']
        ph = [0, 0, 0]
        a_boundary = []
        s_l = 0
        for p in pattern:
            #print("p",p)
            l = 0
            for s in key_idxs[s_l:]:
                l += 1
                #print("key_idxs[:]",key_idxs[s_l:])
                if ph[0] == 0 and s[0] == p:
                    ph[0] = 1
                    s_l = l
                    break
                elif ph[0] == 1 and ph[1] == 0 and s[0] == p:
                    ph[1] = 1
                    s_l = s_l + l
                    break
                elif ph[1] == 1 and ph[2] == 0 and s[0] == p:
                    ph[2] = 1
                    st = s[1]
                    a_boundary = [st, 'e']
                    got_it = 1
                    s_l = s_l + l
                    break
        possible_api, got_it  = check_if_real_hit(a_boundary, s_line)

    if got_it == 0:
        #pattern 2: 11-0-12 >> 11-replace 0-old_api 12-with ``new_api``
        print("checking for pattern 13 ...")
        pattern = ['11', '0', '12']
        ph = [0, 0, 0]
        a_boundary = []
        s_l = 0
        for p in pattern:
            #print("p",p)
            l = 0
            for s in key_idxs[s_l:]:
                l += 1
                #print("key_idxs[:]",key_idxs[s_l:])
                if ph[0] == 0 and s[0] == p:
                    ph[0] = 1
                    s_l = l
                    break
                elif ph[0] == 1 and ph[1] == 0 and s[0] == p:
                    ph[1] = 1
                    s_l = s_l + l
                    break
                elif ph[1] == 1 and ph[2] == 0 and s[0] == p:
                    ph[2] = 1
                    st = s[1]
                    a_boundary = [st, 'e']
                    got_it = 1
                    s_l = s_l + l
                    break
        possible_api, got_it  = check_if_real_hit(a_boundary, s_line)
        
    if got_it == 0:
        #pattern 2: 3-0-10 >> '3-deprecat ... 0-old_api' 10-better ``new_api``
        print("checking for pattern 14 ...")
        pattern = ['3', '0', '10']
        ph = [0, 0, 0]
        a_boundary = []
        s_l = 0
        for p in pattern:
            #print("p",p)
            l = 0
            for s in key_idxs[s_l:]:
                l += 1
                #print("key_idxs[:]",key_idxs[s_l:])
                if ph[0] == 0 and s[0] == p:
                    ph[0] = 1
                    s_l = l
                    break
                elif ph[0] == 1 and ph[1] == 0 and s[0] == p:
                    ph[1] = 1
                    s_l = s_l + l
                    break
                elif ph[1] == 1 and ph[2] == 0 and s[0] == p:
                    ph[2] = 1
                    st = s[1]
                    a_boundary = [st, 'e']
                    got_it = 1
                    s_l = s_l + l
                    break
        possible_api, got_it  = check_if_real_hit(a_boundary, s_line)


    if got_it == 0:
        #pattern 2: 0-16 >> 0-old  16-renamed  <new>
        print("checking for pattern 15 ...")
        pattern = ['0', '16']
        ph = [0, 0]
        a_boundary = []
        s_l = 0
        for p in pattern:
            #print("p",p)
            l = 0
            for s in key_idxs[s_l:]:
                l += 1
                #print("key_idxs[:]",key_idxs[s_l:])
                if ph[0] == 0 and s[0] == p:
                    ph[0] = 1
                    s_l = l
                    break
                elif ph[0] == 1 and ph[1] == 0 and s[0] == p:
                    ph[1] = 1
                    st = s[1]
                    a_boundary = [st, 'e']
                    s_l = s_l + l
                    break
        possible_api, got_it  = check_if_real_hit(a_boundary, s_line)
        
    if got_it == 0:
        #pattern 2: 0-13 >> 0-old_api 13-available in <new api>
        print("checking for pattern 16 ...")
        pattern = ['0', '13']
        ph = [0, 0]
        a_boundary = []
        s_l = 0
        for p in pattern:
            #print("p",p)
            l = 0
            for s in key_idxs[s_l:]:
                l += 1
                #print("key_idxs[:]",key_idxs[s_l:])
                if ph[0] == 0 and s[0] == p:
                    ph[0] = 1
                    s_l = l
                    break
                elif ph[0] == 1 and ph[1] == 0 and s[0] == p:
                    ph[1] = 1
                    st = s[1]
                    a_boundary = [st, 'e']
                    got_it = 1
                    s_l = s_l + l
                    break
        possible_api, got_it  = check_if_real_hit(a_boundary, s_line)
        print(possible_api)
        
    if got_it == 0:
        #pattern 2: 0-3-11 >> 0-old_api 3-deprecat 11-replcemen ``new_api``
        print("checking for pattern 17 ...")
        pattern = ['0', '3', '11']
        ph = [0, 0, 0]
        a_boundary = []
        s_l = 0
        for p in pattern:
            #print("p",p)
            l = 0
            for s in key_idxs[s_l:]:
                l += 1
                #print("key_idxs[:]",key_idxs[s_l:])
                if ph[0] == 0 and s[0] == p:
                    ph[0] = 1
                    s_l = l
                    break
                elif ph[0] == 1 and ph[1] == 0 and s[0] == p:
                    ph[1] = 1
                    s_l = s_l + l
                    break
                elif ph[1] == 1 and ph[2] == 0 and s[0] == p:
                    ph[2] = 1
                    st = s[1]
                    a_boundary = [st, 'e']
                    got_it = 1
                    s_l = s_l + l
                    break
        possible_api, got_it  = check_if_real_hit(a_boundary, s_line)

    if got_it == 0:
        #pattern 2: 0-4-5 >> '0-old_api' ...4-use ``new_api`` 5-instead
        print("checking for pattern 18 ...")
        pattern = ['0', '4', '5']
        ph = [0, 0, 0]
        a_boundary = []
        s_l = 0
        for p in pattern:
            #print("p",p)
            l = 0
            for s in key_idxs[s_l:]:
                l += 1
                #print("key_idxs[:]",key_idxs[s_l:])
                if ph[0] == 0 and s[0] == p:
                    ph[0] = 1
                    s_l = l
                    break
                elif ph[0] == 1 and ph[1] == 0 and s[0] == p:
                    ph[1] = 1
                    st = s[1]
                    s_l = s_l + l
                    break
                elif ph[1] == 1 and ph[2] == 0 and s[0] == p:
                    ph[2] = 1
                    a_boundary = [st, s[1]]
                    got_it = 1
                    #print("st", st)
                    s_l = s_l + l
                    break
        possible_api, got_it  = check_if_real_hit(a_boundary, s_line)

    if got_it == 0:
        #pattern 2: 0-17 >> '0-old_api' .17-'superceded by' ``new_api`` 
        print("checking for pattern 19 ...")
        pattern = ['0', '17']
        ph = [0, 0]
        a_boundary = []
        s_l = 0
        for p in pattern:
            #print("p",p)
            l = 0
            for s in key_idxs[s_l:]:
                l += 1
                #print("key_idxs[:]",key_idxs[s_l:])
                if ph[0] == 0 and s[0] == p:
                    ph[0] = 1
                    s_l = l
                    break
                elif ph[0] == 1 and ph[1] == 0 and s[0] == p:
                    ph[1] = 1
                    st = s[1]
                    a_boundary = [st, 'e']
                    got_it = 1
                    s_l = s_l + l
                    break
        possible_api, got_it  = check_if_real_hit(a_boundary, s_line)


    if got_it == 0:
        #pattern 2: 3-0-2 >> 3-deprecat '0-old_api' 2-replace ``new_api``
        print("checking for pattern 20 ...")
        pattern = ['3', '0', '2']
        ph = [0, 0, 0]
        a_boundary = []
        s_l = 0
        for p in pattern:
            #print("p",p)
            l = 0
            for s in key_idxs[s_l:]:
                l += 1
                #print("key_idxs[:]",key_idxs[s_l:])
                if ph[0] == 0 and s[0] == p:
                    ph[0] = 1
                    s_l = l
                    break
                elif ph[0] == 1 and ph[1] == 0 and s[0] == p:
                    ph[1] = 1
                    s_l = s_l + l
                    break
                elif ph[1] == 1 and ph[2] == 0 and s[0] == p:
                    ph[2] = 1
                    st = s[1]
                    a_boundary = [st, 'e']
                    got_it = 1
                    #print("st", st)
                    s_l = s_l + l
                    break
        possible_api, got_it  = check_if_real_hit(a_boundary, s_line)

    if got_it == 0:
        #pattern 2: 11-15-0 >> <new> 11-replace 15-older '0-old_api' 
        print("checking for pattern 21 ...")
        pattern = ['11', '15', '0']
        ph = [0, 0, 0]
        a_boundary = []
        s_l = 0
        for p in pattern:
            #print("p",p)
            l = 0
            for s in key_idxs[s_l:]:
                l += 1
                #print("key_idxs[:]",key_idxs[s_l:])
                if ph[0] == 0 and s[0] == p:
                    st = 0
                    a_boundary = [st, s[1]]
                    ph[0] = 1
                    s_l = l
                    break
                elif ph[0] == 1 and ph[1] == 0 and s[0] == p:
                    ph[1] = 1
                    s_l = s_l + l
                    break
                elif ph[1] == 1 and ph[2] == 0 and s[0] == p:
                    ph[2] = 1
                    got_it = 1
                    #print("st", st)
                    s_l = s_l + l
                    break
        possible_api, got_it  = check_if_real_hit(a_boundary, s_line)

        
    if(possible_api):
        n_api.append(possible_api)
         
    return n_api
#--------------------------------------------------------------------------------------

def driver_f(depd_api, repl_api = "is706"):
    replacements = []
    words = depd_api.split('.')
    library = words[0]
    
    if mode == 0:
          depd_api = "test.aaa.bbb.ccc.ddd"
          library = "test"
    print("!-- missing api : ", depd_api) 
    print("    searching in directory : ", library)
    file_names = os.listdir("dataRST/"+library)
    
    posible_variants = get_possible_variants(library, depd_api)
    #print(posible_variants)
    #print("    searching by full api name/variants ...")
    for missing_api in posible_variants:
        hits = search_api(library, missing_api, file_names)
        #print("mis api", missing_api, "hits", hits)
        if(len(hits) > 0):
            matched_api = missing_api
            break
    
        
    #search for other variants of the API. eg; for api: a.b.c >> search for: b.c, c    
    if len(hits) == 0:
        extra_variants = split_api_name(depd_api)
        l = len(extra_variants)
        if l > 0:
            #print("    searching by extra variants of the api name ...")
            extra_hits = 0
            r = 0
            while r < l:
                hits = search_api(library, extra_variants[r], file_names)
                if(len(hits) > 0):
                    matched_api = extra_variants[r]
                    break
                r += 1
    ll = len(hits)
    if ll > 0:
        replacements = []
        #print("all hits",hits)
        for item in hits:
            print("\n!-- possible replacement in : ", item[0])
            m = 1
            l = len(item)
            print("!-- deprecation details from release notes ...")
            while m < l:
                print(m, ":", item[m])
                ans = extract_replacement(item[m], matched_api)
                if len(ans) > 0:
                    replacements.append(ans)
                m = m + 1
        if replacements:
            #print("v",replacements)
            #replacements = list(dict.fromkeys(replacements[0]))
            print("\n!-- replacement APIs : ", replacements)
        else:
            print("\n!-- no replacement so far ...")
        
    if result_log == 1:
        if result_log == 1:
            extr = ''
            if hits:
                for h in hits:
                    for hh in h:
                        extr = extr + ' ' + hh
            success = '0'
            hit_in_rst = '0'
            if(hits):
                hit_in_rst = '1'
            r_api = ''
            if repl_api != "is706":
                r_api = r_api+repl_api
            tmp = depd_api+","+r_api+","+hit_in_rst
            r_list = ''
            if(replacements):
                success = '1'
                for rp in replacements:
                    r_list = r_list+" "+str(rp)
            r_list = tmp+","+success+","+r_list+","+extr
            #writer.writerow([r_list])
            f.write(r_list)
            f.write('\n')
            
    print("end------------------------------------------------------\n") 
    
    return replacements
#--------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
# 0-dev test, 
# 2-search one deprecation, 
# 1-search multiples
# 3-fileinput
mode        = 3  
#enable logging of results
result_log  = 1

if result_log == 1:
    f = open('RSTresults.csv', 'a', newline='')
    f.truncate(0)
    r_header = "DEPRECATED_API"+","+"KNOWN_REPLACEMENT"+","+"MENTIONED_IN_REL_NOTES"+","+"REPLACEMENT_FOUND"+","+"PROPOSED_REPLACEMENT"+","+"EXTRACT_FROM_DOCUMENTATION"
    f.write(r_header)
    f.write('\n')
    #writer = csv.writer(f, delimiter=',')

print("!-------------------------------------------------------!") 
#dev test
if mode == 0 :
	mising_api = "teest.test"
	driver_f(mising_api)

#search multiples
if mode == 1:
	missing_apis = ["numpy.alen",
		      "numpy.testing.rand",
		      "numpy.typeDict",
		      "numpy.random.random_integers",
		      "numpy.asscalar"]
	for missing_api in missing_apis:
	    driver_f(missing_api)
        
#search one deprecated API
if mode == 2:
	mising_api = "numpy.alen" #alterdot
	driver_f(mising_api, "len")

#search by providing a file with depd APIs
if mode == 3:
    with open('depdAPI/pandas.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            if len(lines) == 1:
                lines.append("")
            driver_f(lines[0], lines[1])

if result_log == 1:
    f.close()