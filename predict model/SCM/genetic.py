#
# genetic.py
#

import random
import sys
import os # markliou
from multiprocessing import Process,Pool
import itertools
import bisect
MAXIMIZE, MINIMIZE = 11, 22

###########


class Individual(object):
    alleles = (0,1)
    length = 400
    seperator = ''
    optimization = MINIMIZE
    boundMAX = 1000
    boundMIN = 0

    def __init__(self, chromosome=None):
        self.chromosome = chromosome or self._makechromosome()
        self.score = None  # set during evaluation
        self.kfoldacc = 0
        #self.pool=Pool(15)
    
    def _makechromosome(self):
        "makes a chromosome from randomly selected alleles."
        return [random.uniform(self.boundMIN,self.boundMAX) for gene in range(self.length)] 

    def evaluate(self, optimum=None):
        "this method MUST be overridden to evaluate individual fitness score."
        pass
    
    def crossover(self, other):
        "override this method to use your preferred crossover method."
        return self._twopoint(other)
    
    def mutate(self, gene):
        "override this method to use your preferred mutation method."
        self._pick(gene) 
    
    # sample mutation method
    def _pick(self, gene):
        "chooses a random allele to replace this gene's allele."
        self.chromosome[gene] = random.randint(boundMIN,boundMAX)
    
    # sample crossover method
    def _twopoint(self, other):
        "creates offspring via two-point crossover between mates."
        left, right = self._pickpivots()
        def mate(p0, p1):
            chromosome = p0.chromosome[:]
            chromosome[left:right] = p1.chromosome[left:right]
            child = p0.__class__(chromosome)
            child._repair(p0, p1)
            return child
        return mate(self, other), mate(other, self)

    # some crossover helpers ...
    def _repair(self, parent1, parent2):
        "override this method, if necessary, to fix duplicated genes."
        pass

    def _pickpivots(self):
        left = random.randrange(1, self.length-2)
        right = random.randrange(left, self.length-1)
        return left, right

    #
    # other methods
    #

    def __repr__(self):
        "returns string representation of self"
        return '<%s chromosome="%s" score=%s>' % \
               (self.__class__.__name__,
                self.seperator.join(map(str,self.chromosome)), self.score)

    def __cmp__(self, other):
        if self.optimization == MINIMIZE:
            return cmp(self.score, other.score)
        else: # MAXIMIZE
            return cmp(other.score, self.score)
    
    def copy(self):
        twin = self.__class__(self.chromosome[:])
        twin.score = self.score
        return twin


class Environment(object):
    OutFileFlag = 0 ; #markliou
    output_scorecard =""; #markliou
    def __init__(self, kind, population=None, size=20, maxgenerations=100, 
                 crossover_rate=0.90, mutation_rate=0.01, optimum=None):
        #self.pool=Pool(15)
        self.kind = kind
        self.size = size
        self.optimum = optimum
        if not population:
            self.population = self._makepopulation()
        else:
            self.population = population
        #for ind in self.population:
        #    ind.evaluate()
        
        self.gen_score=[]
        self.acc_list=[]
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.maxgenerations = maxgenerations
        self.generation = 0
        
        #self.report()

    
    def evaluate_pop(self):
        #wait of rwrite
        pass
    def _makepopulation(self):
        return [self.kind() for individual in range(self.size)]
    
    def run(self):
        times = 1
        self.evaluate_pop()
        self.population.sort(key=lambda x: ( x.score) ,reverse=True)
        while not self._goal():
            print(times)
            self.step()
            times += 1
        return self.report
    
    def _goal(self):
        return self.generation > self.maxgenerations or \
               self.best.score == self.optimum
    
    def step(self):
        
        if self.generation != 0:
            print('start_optimize')
            self.population.sort(key=lambda x: ( x.score) ,reverse=True)
            self.population = self.population[:self.size]
            self._crossover()
        else:
            self.population.sort(key=lambda x: ( x.score) ,reverse=True)
        self.generation += 1
        self.report()
    
    def _crossover(self):
        next_population = [self.best.copy()]
        i=1
        for mate2 in self._roulette(int(self.size/2)):
            if self.generation == 0:
                mate1 = self.population[0]
            else:
                mate1 = self.best.copy()
            #mate2 = self.population[i+1]
            offspring = mate1.crossover(mate2)
            print('crossover done '+str(i)+'\r',end='')
            i += 1
            self._mutate(offspring[0])
            self._mutate(offspring[1])
            offspring[0].evaluate(self.optimum)
            offspring[1].evaluate(self.optimum)
            next_population.append(offspring[0])
            next_population.append(offspring[1])    
        self.population = next_population

    def _select(self):
        "override this to use your preferred selection method"
        return self._roulette(self.size)
    
    def _mutate(self, individual):
        for gene in range(individual.length):
            if random.random() < self.mutation_rate:
                individual.mutate(gene)

    #
    # sample selection method
    #
    def _tournament(self, size=8, choosebest=0.90):
        competitors = [random.choice(self.population) for i in range(size)]
        competitors.sort()
        if random.random() < choosebest:
            return competitors[0]
        else:
            return random.choice(competitors[1:])
    def _roulette(self, num_parents):
        #Uses code taken from
        #http://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
        
        cumulative_scores = list(itertools.accumulate(member.score for member in self.population[1:]))
        total = cumulative_scores[-1]
        
        for _ in range(num_parents):
            yield self.population[bisect.bisect(cumulative_scores, random.uniform(0, total))]
    def best():
        doc = "individual with best fitness score in population."
        def fget(self):
            self.population.sort(key=lambda c : (c.score) ,reverse=True)
            self.population[0].evaluate()
            return self.population[0]
        
        #return self.population[0]
        return locals()
        
    best = property(**best())

    def report(self):
        
        print ("="*70)
        print ("generation: " + str(self.generation))
        
        #print ("best:       " + str(self.best))
        #print self.best.score
        #print self.best.chromosome
        
        ### markliou for automatic testing existing file
        if self.generation%5==0:
           self.OutFileFlag = 0
        if self.OutFileFlag == 0 :
            ReportFileNo = 1 ;
            self.output_scorecard = "output_scorecard" + str(ReportFileNo)
            while os.path.exists(self.output_scorecard):
                #print('path_exists')
                ReportFileNo = ReportFileNo + 1
                self.output_scorecard = "output_scorecard" + str(ReportFileNo)
            self.OutFileFlag = 1 ;
        f12= open(self.output_scorecard, "w")
        ##### markliou #####
        
        #f12= file("output_scorecard", "w")
        
        best_acc=self.best.kfoldacc
        self.gen_score.append(self.best.score)
        print (self.gen_score)
        self.acc_list.append(best_acc)
        print(self.acc_list)
        f12.write("gen_score:"+"\t"+str(self.gen_score)+"\n")
        f12.write("best CV:"+"\t"+str(best_acc)+"\n")
        f12.write("best scoring:"+"\t"+str(self.best.score)+"\n")
        f12.write("best chromosome:"+"\t"+str(self.best.chromosome)+"\n"+"\n")
        f12.close()
        #print([c.kfoldacc for c in self.population])
        #print([c.score for c in self.population])
        print('kfold acc :' ,end='\t')
        print(str(best_acc))
        print('report done')
        return self.output_scorecard
        


        
