

from icecream import ic

import powfacpy
from powfacpy.pf_class_protocols import *
from powfacpy.pf_elm_objects import create_elm_object, PFElm



class Topology(powfacpy.PFActiveProject):
  
  def __init__(self, pf_app: powfacpy.PFApp):
    super().__init__(pf_app)
    
  @staticmethod
  def get_coherent_group(
    elms, 
    start_elm = None) -> tuple[list[PFGeneral], list[PFGeneral]]:
    boundary_elms = []
    coherent_group = []
    if not start_elm:
      start_elm = elms[0]
    elms = set(elms)  
    connected_elms = start_elm.GetConnectedElements()
    while connected_elms:
      connected_elms = set(connected_elms) - set(coherent_group)
      boundary_elms += list(connected_elms - elms)
      connected_elms = list(connected_elms - set(boundary_elms))
      coherent_group += connected_elms
      for index_elm in range(len(connected_elms)):
        connected_elms += connected_elms[index_elm].GetConnectedElements()
    return coherent_group, boundary_elms
  
  @staticmethod
  def get_coherent_group_from_terminals(terminals: list[PFGeneral]):
    boundary_branch_elms = []
    coherent_group = []
    past_terminals = []
    current_terminals = [terminals[0]]  
    terminals = set(terminals)
    n = 0
    while current_terminals:
      current_terminals: list[PFGeneral] = list(
        set(current_terminals) - set(coherent_group))  
      ic(current_terminals)
      for term_num in range(len(current_terminals)):
        term = current_terminals[term_num]
        ic(term)
        connected_branches = term.GetConnectedElements()
        for branch in connected_branches:
          ic(branch)
          connected_terminals = branch.GetConnectedElements()
          if len(connected_terminals) > 1:
            if len(connected_terminals) - len(set(connected_terminals) - terminals) > 1:
              coherent_group.append(branch)
              current_terminals += [term for term in connected_terminals if term in terminals]
            else:
              boundary_branch_elms.append(branch)  
          else:
            coherent_group.append(branch)      
      n += 1
      if n > 2:
        raise Exception
    

    
class CoherentRegion():
  
  def __init__(self) -> None:
    self.elms: list[PFGeneral]
    self.boundary_branch_elms: list[PFGeneral] = []
    self.boundary_branch_elms_bus_index: list[int] = []
    self.boundary_terminals: list[PFGeneral] = [] 
  
  
  def _add_boundary_elm(self, boundary_elm: PFGeneral):
    if boundary_elm.GetClassName() == "ElmTerm":
      self._add_boundary_terminal(boundary_elm)
    else:
      self._add_boundary_branch_elm(boundary_elm)
    self.boundary_terminals = list(set(self.boundary_terminals))  
    
    
  def _add_boundary_terminal(self, boundary_terminal: ElmTerm):
    self.boundary_terminals.append(boundary_terminal)
    connected_branch_elms = boundary_terminal.GetConnectedElements()
    for connected_branch_elm in connected_branch_elms:
      if connected_branch_elm in self.elms:
        self.boundary_branch_elms.append(connected_branch_elm)
        connected_branch_elm = create_elm_object(connected_branch_elm)
        self.boundary_branch_elms_bus_index.append(connected_branch_elm.get_bus_index_of_terminal(boundary_terminal))
        
              
  def _add_boundary_branch_elm(self, boundary_branch_elm: PFGeneral):
      boundary_branch_elm = create_elm_object(boundary_branch_elm)
      for bus_index, connecting_terminal in enumerate(boundary_branch_elm.get_connected_elms_ordered()):
        if connecting_terminal in self.elms:
          self.boundary_branch_elms.append(boundary_branch_elm.pf_obj)   
          self.boundary_branch_elms_bus_index.append(bus_index)
          self.boundary_terminals.append(connecting_terminal)
      
        

    
          
            


          

       
