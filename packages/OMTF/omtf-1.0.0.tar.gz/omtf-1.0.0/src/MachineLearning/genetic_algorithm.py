
import numpy as np
import matplotlib.pyplot as plt

class GeneticAlgorithm:
    
    class Transformations:
        MUTATION = 'mutation'
        TRANSFORMATION = 'transformation'
    
    def __init__(
        self,
        n_variables:int,
        n_genes:int,
        n_iterations:int,
        transformation_type:Transformations = None,
        mutation_type = None,
        crossover_type = None,
        gene_selection_type = None,
        n_selected_individuals:int = None,
        n_candidates:int = None,
        random_state = None, 
        gene_limits = None,
        fitness_func = None
        ) -> None:

        # Make validations
        if transformation_type not in ['mutation', 'transformation']:
            raise ValueError('transformation_type should be one of mutation or transformation.')

        self.n_variables = n_variables
        self.n_genes = n_genes
        self.gene_limits = gene_limits 
        self.transformation_type = transformation_type
        self.mutation_type = mutation_type
        self.random_state = random_state
        self.fitness_func = fitness_func
        self.n_iterations = n_iterations
        self.gene_selection_type = gene_selection_type
        self.n_selected_individuals = n_selected_individuals
        self.n_candidates = n_candidates
        self.crossover_type = crossover_type
        self.best_fitness_evolution = []

        # Asserts 
        # Check that fitness function is a function
        assert callable(fitness_func)
    
        # Create the population
        if self.gene_limits is not None:
            
            # Check that both vectors have the same length
            assert len(self.gene_limits) == self.n_variables

            limits = [np.random.uniform(limit[0], limit[1], self.n_genes)
                for limit in self.gene_limits] 

        else:
            limits = [np.random.random(self.n_genes)
                for limit in range(self.n_variables)]
        
        # Convert list of limits to list of solutions
        self.population = np.array(list(zip(*limits)))

    def get_fitness_scores(self):
        scores = [self.fitness_func(ind) for ind in self.population]
        scores = np.array(scores)
        return scores 

    def __append_best_score(self, scores):
        best_score = np.max(scores)
        self.best_fitness_evolution.append(best_score)
        return 'Ok'


    def __ranking_selection(self, k):
        if k is None:
            raise ValueError('K must not be none if type ranking is selected.')
        
        ind = np.argpartition(self.get_fitness_scores(), k)[-k:]
        return ind

    def __tournament_selection(self, k, n_candidates):
        candidates = [np.random.randint(0, len(self.get_fitness_scores()), 3) for i in range(3)]
        tournament_winner = [np.argmax(self.get_fitness_scores()[tournament]) for i, tournament in enumerate(candidates)]
        ind = [tournament[tournament_winner[i]] for i, tournament in enumerate(candidates)]

        return np.array(ind)

    def gene_selection(self, gene_selection_type, k, n_candidates = None):

        if gene_selection_type not in ['ranking','tournament']:
            raise ValueError('Type should be ranking or tournament')
        
        if gene_selection_type == 'ranking':
            ind = self.__ranking_selection(k)
        elif gene_selection_type == 'tournament':
            ind = self.__tournament_selection(k, n_candidates)
        else:
            pass

        return ind
    
    def __crossover(self, parent1, parent2, crossover_type):
        
        # Check crossover type
        if crossover_type not in ['uniform', 'one_point']:
            raise ValueError('crossover_type should be one of uniform, one_point or multi_point')
        
        if crossover_type == 'one_point':
            index = np.random.choice(range(len(parent1)))
            children = parent2[:index] + parent1[index:], parent1[:index] + parent2[index:]

        elif crossover_type == 'uniform':
            parents = list(zip(*[parent1,parent2]))
            children1 = tuple([np.random.choice(element) for element in parents])
            children2 = tuple([np.random.choice(element) for element in parents])
            children = children1, children2
        else:
            pass

        return children


    def __mutation(self, individual, mutation_type):

        if mutation_type not in ['bitstring', 'shrink']:
            raise ValueError('mutation_type should be one of bitstring or shrinkg')
        
        # Get index of individual to modify
        index = np.random.choice(len(individual))

        # Convert individual to list so that can be modified
        individual_mod = list(individual)

        if mutation_type == 'bitstring':      
            individual_mod[index] = 1 - individual_mod[index]
        
        else:
            individual_mod[index] = individual_mod[index] + np.random.rand()
        
        # Convert indivudal to tuple
        individual = tuple(individual_mod)

        return individual

    def optimize(self):
        
        for i in range(self.n_iterations):

            # Calculate fitness score
            scores = self.get_fitness_scores()

            # Append best score
            _ = self.__append_best_score(scores)

            # Make Selection
            selected_genes = self.gene_selection(
                gene_selection_type = self.gene_selection_type,
                k = self.n_selected_individuals,
                n_candidates = self.n_candidates
                )
            
            # Get selected population
            selected_population = self.population[selected_genes.tolist()]
            

            # Make transformations (mutation/crossover)
            if self.transformation_type == 'mutation':
                transformed_genes_index = np.random.choice(
                    range(len(selected_population)),
                    self.n_genes
                    )
                

                new_population = [self.__mutation(selected_population[i], self.mutation_type)
                for i in transformed_genes_index]
            
            else:
                # Get pairs of parents
                parents_pairs = np.random.choice(
                    selected_genes,
                    (int(self.n_genes/2),2)
                    )
                
                # For each pair, make crossover
                new_population = [self.__crossover(self.population[parents[0]],
                                                self.population[parents[1]],
                                                crossover_type=self.crossover_type
                                                )
                for parents in parents_pairs]
                
                # Unnest population
                new_population = [child for children in new_population for child in children]
            
            # Set new population as population
            self.population = np.array(new_population)
        
        # When n_iterations are finished, fitness score
        scores = self.get_fitness_scores()

        # Append best score
        _ = self.__append_best_score(scores)

        # Get the result where the result is the best
        best_score_ind =np.argpartition(scores, 0)[0]
        
        best_solution = self.population[best_score_ind]

        return (best_solution, self.best_fitness_evolution[-1])

    def view_fitness_evolution(self):
        plt.plot(
            range(len(self.best_fitness_evolution)),
            self.best_fitness_evolution
        )


def fitness_func(solution:np.ndarray, margin:np.ndarray=np.array([2, 2.5]),
                 material_consumption:np.ndarray=np.array([2,3]),
                 material_max:int=500) -> float:

    solution = np.array(solution)
    solution_added = solution + 50
    calculated_margin = np.sum(solution_added*margin)
    material_consumed = np.sum(solution_added*material_consumption)
    
    return 0 if material_consumed > material_max else calculated_margin

if __name__ == '__main__':

    ga = GeneticAlgorithm(
        n_variables = 2,
        n_genes = 10,
        n_iterations = 50,
        transformation_type = 'mutation', #transformation
        mutation_type = 'shrink',
        #crossover_type = 'uniform',
        gene_selection_type = 'ranking',
        n_selected_individuals = 3,
        #n_candidates = None,
        #random_state = None, 
        #gene_limits = None,
        fitness_func = fitness_func
    )

    print(ga.optimize())
    ga.view_fitness_evolution()

    ga = GeneticAlgorithm(
        n_variables = 2,
        n_genes = 10,
        n_iterations = 50,
        transformation_type = 'transformation',
        crossover_type = 'uniform',
        gene_selection_type = 'ranking',
        n_selected_individuals = 3,
        fitness_func = fitness_func
    )

    print(ga.optimize())
    ga.view_fitness_evolution()