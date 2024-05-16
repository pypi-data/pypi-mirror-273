################################################################################
#
# solid_dmft - A versatile python wrapper to perform DFT+DMFT calculations
#              utilizing the TRIQS software library
#
# Copyright (C) 2018-2020, ETH Zurich
# Copyright (C) 2021, The Simons Foundation
#      authors: A. Hampel, M. Merkel, and S. Beck
#
# solid_dmft is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# solid_dmft is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with
# solid_dmft (in the file COPYING.txt in this directory). If not, see
# <http://www.gnu.org/licenses/>.
#
################################################################################

version = "3.2.3"
triqs_hash = "8216931d15230ad4ffd4acba3db651046c040d99"
solid_dmft_hash = "5a6299a234bc906a59921f32e93962a91d2c59cc"

def show_version():
  print("\nYou are using solid_dmft version %s\n"%version)

def show_git_hash():
  print("\nYou are using solid_dmft git hash %s based on triqs git hash %s\n"%("5a6299a234bc906a59921f32e93962a91d2c59cc", triqs_hash))
