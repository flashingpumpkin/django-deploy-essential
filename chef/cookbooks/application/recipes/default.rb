home = "/home/#{node[:user]}"

# Some handy defaults
template "#{home}/.pythonrc" do
	source "pythonrc.erb"
	action :create
	owner node[:user]
end

# More handy defaults
template "#{home}/.bashrc" do
	source "bashrc.erb"
	action :create
	owner node[:user]
end
