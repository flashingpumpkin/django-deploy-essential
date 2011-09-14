
node[:groups].each do |group|
	group group[:id] do
		group_name group[:id]
		action [:create, :modify, :manage]
	end
end

node[:users].each do |user|
	home = user[:home] || "/home/#{user[:id]}"

	user user[:id] do
		comment user[:comment]
		home home
		shell user[:shell] || "/bin/bash"
		supports :manage_home => true
		action [:create, :manage]
	end

	directory "#{home}/.ssh" do
		action :create
		owner user[:id]
		mode 0700
	end

	template "#{home}/.ssh/authorized_keys" do
		source "authorized_keys.erb"
		action :create
		owner user[:id]
		variables(:keys => user[:authorized_keys])
	end
	
end
