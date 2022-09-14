import random
import math
from wave_function_package import Patch

class WaveElement:
    """Represents a single location in the wave function as a super-position of Patches.
    
    Attributes
    ----------
    normalization : int
        Weighted number of Patches still possible
    patches : dict {<int> : list <Patch>}
        The dictionary of Patches in super-position, indexed by Patch.core
    possible_cores : list <int>
        List of cores that are still possible
    collapsed : bool
        True when the WaveElement has collapsed to a core, False otherwise
    selected_core : int
        If the WaveElement has collapsed, this is the core of the remaining Patches
        """
    
    def __init__(self, all_patches = []):
        """
        Parameters
        ----------
        all_patches : list <Patch>
            List of all Patches to be put in super-position
        """
        
        self.normalization = 0
        self.patches = {}
        self.possible_cores = []
        self.collapsed = False
        self.selected_core = -1
        for p in all_patches:
            self.add_patch(p)
            
    def add_patch(self, patch):
        """Adds one Patch to the super-position, updating values accordingly
        
        Parameters
        ----------
        patch : Patch
            A single Patch
        """
        
        if self.collapsed:
            raise Exception("calling add_patch despite being collapsed");
        if patch.core not in self.patches:
            self.patches[patch.core] = []
        self.patches[patch.core].append(patch)
        self.normalization = self.normalization + patch.frequency
        if patch.core not in self.possible_cores:
            self.possible_cores.append(patch.core)
            
    def subtract_patch(self, patch):
        """Removes one Patch to the super-position, updating values accordingly
        
        Parameters
        ----------
        patch : Patch
            A single Patch
        """
        
        if self.collapsed:
            raise Exception("calling subtract_patch despite being collapsed");
        kill_list = []
        if patch.core in self.patches:
            for p in self.patches[patch.core]:
                if p.same_pattern(patch):
                    self.normalization = self.normalization - p.frequency
                    kill_list.append(p)
        
        for k in kill_list:
            self.patches[patch.core].remove(k)
        if len(self.patches[patch.core]) == 0:
            self.possible_cores.remove(patch.core)
            
    def get_collapse_quality(self):
        """Calculates the quality of the collapse of this WaveElement.
        
        Quality should mathematically be shannon entropy, but for a 2d 
        wave function collapse, normalization is used for simplicity.
        """
        
        if self.collapsed:
            raise Exception("calling get_collapse_quality despite being collapsed");
                    
        #    Shannon Entropy
        
        #sum_weight = 0
        #sum_weight_log = 0
        #for c in self.patches:
        #    part_sum = 0
        #    for p in self.patches[c]:
        #        part_sum = part_sum + p.frequency
        #    if part_sum > 0:
        #        sum_weight = sum_weight + part_sum
        #        sum_weight_log = sum_weight_log + part_sum*math.log(part_sum)
        #entropy = 100
        #if sum_weight > 0:
        #    entropy = math.log(sum_weight) - (sum_weight_log / sum_weight)
        #
        #return entropy
        
        
        return self.normalization        
    
    def fixed_collapse(self, core):
        """Collapses the WaveElement to the chosen core.
        
        Parameters
        ----------
        core : int
            The core to collapse to
        """
        
        if self.collapsed:
            raise Exception("calling fixed_collapse despite being collapsed");
        self.collapsed = True
        self.selected_core = core
        self.normalization = 1
        self.patches = {}
        self.possible_cores = [self.selected_core]
        
    def max_collapse(self):
        """Collapses the WaveElement to the core of the highest frequency Patch.
        """
        
        if self.collapsed:
            raise Exception("calling max_collapse despite being collapsed");
        if len(self.patches) == 0:
            raise Exception("Failed max_collapse : No patches")
        max_patch = None
        max_freq = -1
        for c in self.patches:
            for p in self.patches[c]:
                if p.frequency >= max_freq:
                    max_patch = p
                    max_freq = p.frequency
        self.fixed_collapse(max_patch.core)
        
    def max_core_collapse(self):
        """Collapses the WaveElement to the core with the total highest frequency.
        """
        
        if self.collapsed:
            raise Exception("calling max_core_collapse despite being collapsed");
            
        if len(self.patches) == 0:
            raise Exception("Failed max_core_collapse : No patches")
            
        max_core = -1
        max_freq = -1
        for c in self.patches:
            total = 0
            for p in self.patches[c]:
                total = total + p.frequency
            if total >= max_freq:
                max_core = c
                max_freq = total
        self.fixed_collapse(max_core)
        
    def probable_collapse(self):
        """Collapses the WaveElement via probability, weighted to each Patch by its frequency.
        """
        
        if self.collapsed:
            raise Exception("calling probable_collapse despite being collapsed");
            
        countdown = random.randint(0,self.normalization)
        for c in self.patches:
            for p in self.patches[c]:
                countdown = countdown - p.frequency
                if countdown <= 0:
                    self.fixed_collapse(p.core)
                    return
        raise Exception("Failed probable_collapse : Countdown did not end")
        
    def cull_patches(self, surroundings):
        """Removes Patches from the super-position based on surroundings.
        
        Parameters
        ----------
        surroundings : list <WaveElement>
            The possible wave surrounding this WaveElement.
        
        Returns
        -------
        bool
            If this culling changed the super-position.
        """
        
        if self.collapsed:
            raise Exception("calling cull_patches despite being collapsed");
            
        change = False
        for c in self.patches:
            kill_patches = []
            for p in self.patches[c]:
                if not p.match_surroundings(surroundings):
                    kill_patches.append(p)
            for p in kill_patches:
                change = True
                self.subtract_patch(p)
        return change
    
    def check_collapse(self):
        """Test if this WaveElement is collapse, or if it should be, and collapse if so.
        
        Returns
        -------
        bool
            If this WaveElement is now collapsed.
        """
        
        if self.collapsed:
            return True
        if len(self.possible_cores) == 1:
            self.fixed_collapse(self.possible_cores[0])
            return True
        return False
            
        